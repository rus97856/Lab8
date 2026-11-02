import heapq
import math
from itertools import count
from collections import Counter


def build_huffman(freq):
    if not freq:
        raise ValueError("Пустой алфавит")
    order = count()
    heap = [(w, next(order), s) for s, w in freq.items() if w > 0]
    heapq.heapify(heap)
    if not heap:
        raise ValueError("Все частоты нулевые")
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(order), (left, right)))
    tree = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if isinstance(node, str):
            codes[node] = prefix or "0"
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")

    walk(tree)
    return tree, codes


def stats(freq, codes):
    total = sum(freq.values())
    H = abs(sum(w / total * math.log2(w / total) for w in freq.values()))
    L = sum(w / total * len(codes[s]) for s, w in freq.items())
    eta = H / L * 100
    return H, L, eta


def encode(text, codes):
    return "".join(codes[s] for s in text)


def decode(bits, tree):
    if isinstance(tree, str):
        if any(b != "0" for b in bits):
            raise ValueError("Некорректный битовый поток")
        return tree * len(bits)
    result, node = [], tree
    for b in bits:
        if b not in "01":
            raise ValueError("Недопустимый бит")
        node = node[int(b)]
        if isinstance(node, str):
            result.append(node)
            node = tree
    if node is not tree:
        raise ValueError("Неполное кодовое слово")
    return "".join(result)


def test(text):
    freq = Counter(text)
    tree, codes = build_huffman(freq)
    bits = encode(text, codes)
    H, L, eta = stats(freq, codes)
    print("Текст:", text)
    print("Частоты:", dict(freq))
    print("Коды:", codes)
    print(f"H(X) = {H:.4f}, L = {L:.4f}, η = {eta:.2f} %")
    print("Биты:", bits, f"({len(bits)} бит)")
    print("Декодирование:", decode(bits, tree))
    assert decode(encode(text, codes), tree) == text
    print("decode(encode(text)) == text: OK")
    print()


test("ABCADE")
test("AAAA")
