import heapq
import math
from itertools import count
from collections import Counter


def build_huffman(freq):
    order = count()
    heap = [(w, next(order), s) for s, w in freq.items()]
    heapq.heapify(heap)
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


def decode(bits, tree):
    result, node = [], tree
    for b in bits:
        node = node[int(b)]
        if isinstance(node, str):
            result.append(node)
            node = tree
    return "".join(result)


text = (
    "Теория информации изучает количественные закономерности передачи, "
    "хранения и обработки информации. Одной из важнейших задач является "
    "сжатие данных без потерь. Код Хаффмана позволяет построить оптимальный "
    "префиксный код, в котором часто встречающиеся символы получают короткие "
    "кодовые слова, а редкие символы получают длинные кодовые слова. "
    "Благодаря этому средняя длина кода приближается к энтропии источника."
)

print("Длина текста:", len(text), "символов")
print("Учитываются пробелы, регистр и знаки препинания")
print()

freq = Counter(text)
tree, codes = build_huffman(freq)
N = len(text)

print("Символ  n   p       Код")
for s, n in freq.most_common():
    print(f"{repr(s):<7} {n:<3} {n / N:.4f}  {codes[s]}")
print()

H = -sum(n / N * math.log2(n / N) for n in freq.values())
L = sum(n / N * len(codes[s]) for s, n in freq.items())
eta = H / L * 100
R = (1 - H / L) * 100

print(f"Уникальных символов: {len(freq)}")
print(f"H(X) = {H:.4f} бит/символ")
print(f"L = {L:.4f} бит/символ")
print(f"η = {eta:.2f} %")
print(f"R = {R:.2f} %")
print()

bits = "".join(codes[s] for s in text)
padding = (8 - len(bits) % 8) % 8
packed = int(bits + "0" * padding, 2).to_bytes((len(bits) + padding) // 8, "big")

utf8_bits = len(text.encode("utf-8")) * 8
table_bits = sum(len(s.encode("utf-8")) * 8 + 8 + len(c) for s, c in codes.items())
padding_info_bits = 8
total_bits = len(packed) * 8 + table_bits + padding_info_bits

print(f"Объём UTF-8: {utf8_bits} бит ({utf8_bits // 8} байт)")
print(f"Битовый поток Хаффмана: {len(bits)} бит")
print(f"Выравнивание последнего байта: {padding} бит")
print(f"Упаковано в байты: {len(packed)} байт")
print(f"Таблица кодов (символ UTF-8 + 1 байт длины + биты кода): {table_bits} бит")
print(f"Байт с числом битов выравнивания: {padding_info_bits} бит")
print(f"Итого с накладными расходами: {total_bits} бит ({math.ceil(total_bits / 8)} байт)")
print()

print(f"Kс без накладных расходов = {utf8_bits / (len(packed) * 8):.3f}")
print(f"S без накладных расходов = {(1 - len(packed) * 8 / utf8_bits) * 100:.2f} %")
print(f"Kс с накладными расходами = {utf8_bits / total_bits:.3f}")
print(f"S с накладными расходами = {(1 - total_bits / utf8_bits) * 100:.2f} %")
print()

restored = decode(bits, tree)
assert restored == text
print("Декодирование совпадает с исходным текстом: OK")
