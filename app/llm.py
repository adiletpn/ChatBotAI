"""Клиент языковой модели.

Поддерживает два протокола:
  * openai    — POST {base}/chat/completions (OpenAI, xKiro/kiro-прокси, OpenRouter, Groq, Ollama ...)
  * anthropic — POST {base}/messages
Ответ отдаётся потоком (по кусочкам), чтобы в интерфейсе текст «печатался» в реальном времени.
"""
import base64
import json
import logging
import time
from typing import AsyncIterator

import httpx

from .config import settings


log = logging.getLogger(__name__)


class LLMError(RuntimeError):
    pass


# ---------------------------------------------------------------- цепочка моделей

_dead: dict[str, float] = {}  # модель → до какого времени её не пробовать (пропала из каталога)
DEAD_FOR = 1800


def _chain(model: str | None = None) -> list[str]:
    """Основная модель, затем запасные; модели, которых нет в каталоге, пропускаем полчаса."""
    first = model or settings.llm_model
    chain = [first] + [m for m in settings.llm_fallback_models if m != first]
    alive = [m for m in chain if _dead.get(m, 0) < time.time()]
    return alive or chain


def _failed(model: str, error: str) -> None:
    text = error.lower()
    if "http 404" in text or "does not exist" in text or "not found" in text:
        _dead[model] = time.time() + DEAD_FOR
    log.warning("Модель %s не ответила (%s) — пробую запасную", model, error[:160])



def _headers() -> dict:
    if settings.llm_provider == "anthropic":
        return {
            "x-api-key": settings.llm_api_key,
            "Authorization": f"Bearer {settings.llm_api_key}",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    return {"Authorization": f"Bearer {settings.llm_api_key}", "Content-Type": "application/json"}


def _url() -> str:
    path = "/messages" if settings.llm_provider == "anthropic" else "/chat/completions"
    return settings.llm_base_url + path


def _payload(system: str, messages: list[dict], stream: bool, max_tokens: int | None, temperature: float | None,
             model: str | None = None) -> dict:
    model = model or settings.llm_model
    max_tokens = max_tokens or settings.llm_max_tokens
    temperature = settings.llm_temperature if temperature is None else temperature
    if settings.llm_provider == "anthropic":
        return {
            "model": model,
            "system": system,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": stream,
        }
    return {
        "model": model,
        "messages": [{"role": "system", "content": system}, *messages],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
    }


def _extract_text(data: dict) -> str:
    if settings.llm_provider == "anthropic":
        return "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")
    choices = data.get("choices") or []
    if not choices:
        return ""
    return (choices[0].get("message") or {}).get("content") or ""


def _extract_delta(event: dict) -> str:
    if settings.llm_provider == "anthropic":
        if event.get("type") == "content_block_delta":
            return (event.get("delta") or {}).get("text", "")
        return ""
    choices = event.get("choices") or []
    if not choices:
        return ""
    return (choices[0].get("delta") or {}).get("content") or ""


async def _stream_once(payload: dict) -> AsyncIterator[str]:
    # read — пауза между кусочками ответа: «зависшую» модель бросаем через 45 с, а не через 2 минуты
    timeout = httpx.Timeout(settings.llm_timeout, connect=10, read=min(45.0, settings.llm_timeout))
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            async with client.stream("POST", _url(), headers=_headers(), json=payload) as resp:
                if resp.status_code >= 400:
                    body = (await resp.aread()).decode("utf-8", "ignore")[:500]
                    raise LLMError(f"HTTP {resp.status_code}: {body}")
                content_type = resp.headers.get("content-type", "")
                if "text/event-stream" not in content_type:
                    # Сервер проигнорировал stream=true и вернул обычный JSON
                    data = json.loads(await resp.aread())
                    text = _extract_text(data)
                    if text:
                        yield text
                    return
                async for line in resp.aiter_lines():
                    line = line.strip()
                    if not line.startswith("data:"):
                        continue
                    chunk = line[5:].strip()
                    if chunk == "[DONE]":
                        break
                    try:
                        event = json.loads(chunk)
                    except json.JSONDecodeError:
                        continue
                    if "error" in event and event.get("type") != "content_block_delta":
                        raise LLMError(str(event["error"])[:500])
                    delta = _extract_delta(event)
                    if delta:
                        yield delta
        except httpx.HTTPError as exc:
            raise LLMError(f"{type(exc).__name__}: {exc}") from exc


async def stream_chat(system: str, messages: list[dict], max_tokens: int | None = None,
                      temperature: float | None = None, model: str | None = None) -> AsyncIterator[str]:
    """Отдаёт ответ модели по кусочкам. Если модель недоступна до первого слова — переходит к запасной."""
    error = None
    for name in _chain(model):
        started = False
        try:
            async for delta in _stream_once(_payload(system, messages, True, max_tokens, temperature, name)):
                started = True
                yield delta
            return
        except LLMError as exc:
            if started:  # ответ уже печатается — подменить модель посреди текста нельзя
                raise
            _failed(name, str(exc))
            error = exc
    raise error or LLMError("Нет доступных моделей")


async def complete(system: str, messages: list[dict], max_tokens: int | None = None,
                   temperature: float | None = None) -> str:
    """Обычный (не потоковый) запрос — для служебных задач: перевод запроса, резюме, тест."""
    timeout = httpx.Timeout(settings.llm_timeout, connect=10)
    error = None
    for name in _chain():
        payload = _payload(system, messages, False, max_tokens, temperature, name)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(_url(), headers=_headers(), json=payload)
            if resp.status_code >= 400:
                raise LLMError(f"HTTP {resp.status_code}: {resp.text[:500]}")
            return _extract_text(resp.json()).strip()
        except httpx.HTTPError as exc:
            error = LLMError(f"{type(exc).__name__}: {exc}")
        except LLMError as exc:
            error = exc
        _failed(name, str(error))
    raise error or LLMError("Нет доступных моделей")


VISION_PROMPT = (
    "Transcribe ALL text from this scanned document image exactly as written, "
    "keeping the original language (Kazakh, Russian or English) and line structure. "
    "Output only the transcribed text, nothing else."
)


def image_part(data: bytes, mime: str = "image/png") -> dict:
    """Изображение как часть сообщения — в формате нужного протокола."""
    b64 = base64.b64encode(data).decode()
    if settings.llm_provider == "anthropic":
        return {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}}
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}


def vision_transcribe(png_bytes: bytes) -> str:
    """Распознаёт текст на изображении через мультимодальную модель (синхронно — вызывается из потока OCR)."""
    b64 = base64.b64encode(png_bytes).decode()
    if settings.llm_provider == "anthropic":
        content = [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
            {"type": "text", "text": VISION_PROMPT},
        ]
    else:
        content = [
            {"type": "text", "text": VISION_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
        ]
    error = None
    for name in _chain(settings.vision_model):
        payload = _payload("You are a precise OCR engine.", [{"role": "user", "content": content}], False, 4000, 0, name)
        try:
            with httpx.Client(timeout=httpx.Timeout(settings.llm_timeout, connect=10)) as client:
                resp = client.post(_url(), headers=_headers(), json=payload)
            if resp.status_code < 400:
                return _extract_text(resp.json()).strip()
            error = LLMError(f"HTTP {resp.status_code}: {resp.text[:300]}")
        except httpx.HTTPError as exc:
            error = LLMError(f"{type(exc).__name__}: {exc}")
        _failed(name, str(error))
    raise error or LLMError("Нет доступных моделей")


async def check() -> dict:
    """Проверка подключения к LLM (для страницы статуса)."""
    if not settings.llm_enabled:
        return {"ok": False, "error": "LLM_API_KEY не задан — офлайн-режим"}
    try:
        text = await complete("Reply with one word.", [{"role": "user", "content": "ping"}], max_tokens=10)
        return {"ok": True, "reply": text[:50]}
    except LLMError as exc:
        return {"ok": False, "error": str(exc)[:300]}
