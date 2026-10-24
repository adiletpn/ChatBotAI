"""Поиск релевантных фрагментов: алгоритм BM25 + упрощённый стемминг.

Казахский язык агглютинативный (чемпионат-қа, чемпионат-тың, чемпионат-тар-ға),
русский — флективный (документ-ов, документ-ами). Поэтому слова приводятся
к основе обрезкой до первых 6 символов — простой и надёжный приём для обоих языков.
"""
import math
import re
from collections import Counter

STEM_LEN = 6
_WORD = re.compile(r"\w+", re.UNICODE)

STOPWORDS = {
    # ru
    "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то", "все", "она", "так", "его",
    "но", "да", "ты", "к", "у", "же", "вы", "за", "бы", "по", "только", "ее", "мне", "было", "вот", "от",
    "меня", "еще", "нет", "о", "из", "ему", "ли", "если", "или", "ни", "быть", "был", "до", "вас", "уже",
    "для", "это", "этот", "эти", "при", "под", "над", "об", "какой", "какие", "какая", "каких", "есть", "ли",
    "кто", "где", "когда", "сколько", "почему", "зачем", "можно", "нужно", "ли",
    # kk
    "және", "мен", "бен", "пен", "да", "де", "та", "те", "бұл", "осы", "сол", "ол", "үшін", "бойынша",
    "қандай", "қанша", "қашан", "қайда", "кім", "не", "ма", "ме", "ба", "бе", "па", "пе", "немесе", "туралы",
    "болып", "болады", "бар", "жоқ", "ал", "әр", "барлық", "тиіс", "қажет",
    # en
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "is", "are", "was", "were", "be", "by",
    "with", "what", "which", "who", "when", "where", "how", "why", "do", "does", "can", "it", "this", "that",
    "as", "at", "from", "about",
}


VOWELS = set("аеиоуыэюяьйіәөұүaeiouy")


def stem(word: str) -> str:
    word = word[:STEM_LEN]
    # каска / каски / каску → каск
    if len(word) >= 5 and word[-1] in VOWELS:
        word = word[:-1]
    return word


def tokenize(text: str) -> list[str]:
    tokens = []
    for word in _WORD.findall(text.lower().replace("ё", "е")):
        if word in STOPWORDS or (len(word) < 2 and not word.isdigit()):
            continue
        tokens.append(stem(word))
    return tokens


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.chunks: list[dict] = []
        self.tfs: list[Counter] = []
        self.lengths: list[int] = []
        self.df: Counter = Counter()
        self.avg_len = 0.0

    def build(self, chunks: list[dict]) -> None:
        self.chunks = chunks
        self.tfs, self.lengths, self.df = [], [], Counter()
        for chunk in chunks:
            tokens = tokenize(chunk["text"])
            tf = Counter(tokens)
            self.tfs.append(tf)
            self.lengths.append(len(tokens))
            self.df.update(tf.keys())
        self.avg_len = (sum(self.lengths) / len(self.lengths)) if self.lengths else 0.0

    def _idf(self, term: str, n: int) -> float:
        df = self.df.get(term, 0)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def search(self, query: str, top_k: int = 6, allowed_docs: set[str] | None = None) -> list[tuple[dict, float]]:
        terms = tokenize(query)
        if not terms or not self.chunks:
            return []
        n = len(self.chunks)
        q_terms = Counter(terms)
        results = []
        for i, chunk in enumerate(self.chunks):
            if allowed_docs is not None and chunk["doc_id"] not in allowed_docs:
                continue
            tf = self.tfs[i]
            score = 0.0
            length = self.lengths[i] or 1
            for term, q_count in q_terms.items():
                f = tf.get(term)
                if not f:
                    continue
                denom = f + self.k1 * (1 - self.b + self.b * length / (self.avg_len or 1))
                score += self._idf(term, n) * f * (self.k1 + 1) / denom * (1 + 0.2 * (q_count - 1))
            if score > 0:
                results.append((chunk, score))
        results.sort(key=lambda item: item[1], reverse=True)
        return results[:top_k]
