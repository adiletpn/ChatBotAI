"""Фильтр бессмысленных запросов: «р», «???», «фывфыв», «ааааааа».

Проверка локальная и мгновенная — такой запрос не отправляется модели и не тратит дневной лимит.
Повторяющиеся бессмысленные запросы считаются нарушением правил: предупреждение, затем
временное ограничение вопросов (см. UserStore.strike).
"""
import re

VOWELS = set("аеёиоуыэюяәіөұүaeiouyі")
KEYBOARD_ROWS = ["йцукенгшщзхъ", "фывапролджэ", "ячсмитьбю", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def _keyboard_mash(word: str) -> bool:
    """4+ соседние клавиши подряд («фыва», «asdf») или слово из повторов одного кусочка («фывфыв»)."""
    if re.fullmatch(r"(.{2,4})\1+.{0,3}", word):
        return True
    for row in KEYBOARD_ROWS:
        # «пролонгация» содержит «прол», но это слово: почти все буквы должны быть из одного ряда
        if sum(c in row for c in word) / len(word) < 0.8:
            continue
        for i in range(len(row) - 3):
            if row[i:i + 4] in word or row[i:i + 4][::-1] in word:
                return True
    return False


def is_junk(text: str) -> bool:
    text = text.strip().lower()
    words = _WORD.findall(text)
    letters = sum(len(w) for w in words)
    if letters < 3:  # «р», «??», «12», «ок»
        return True
    if re.search(r"(.)\1{4,}", text):  # «аааааа», «!!!!!!»
        return True
    long_words = [w for w in words if len(w) >= 4]
    if long_words and all(not (set(w) & VOWELS) or _keyboard_mash(w) for w in long_words):
        return True  # «фывфыв», «ыжвл», «asdfgh»
    return False
