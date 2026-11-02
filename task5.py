import heapq
import math
from itertools import count


def build_huffman(freq):
    order = count()
    heap = [(w, next(order), s) for s, w in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        w1, _, left = heapq.heappop(heap)
        w2, _, right = heapq.heappop(heap)
        print(f"Объединение: {left} ({w1:.2f}) + {right} ({w2:.2f}) = {w1 + w2:.2f}")
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


p = {"A": 0.40, "B": 0.20, "C": 0.20, "D": 0.10, "E": 0.10}
tree, codes = build_huffman(p)

print()
print("Символ  p     Код    l  p*l")
for s in p:
    print(f"{s:<7} {p[s]:<5} {codes[s]:<6} {len(codes[s])}  {p[s] * len(codes[s]):.2f}")

H = -sum(pi * math.log2(pi) for pi in p.values())
L = sum(p[s] * len(codes[s]) for s in p)
eta = H / L * 100
R = (1 - H / L) * 100

print()
print(f"H(X) = {H:.4f} бит/символ")
print(f"L = {L:.4f} бит/символ")
print(f"η = {eta:.2f} %")
print(f"R = {R:.2f} %")
print(f"η + R = {eta + R:.2f} %")
