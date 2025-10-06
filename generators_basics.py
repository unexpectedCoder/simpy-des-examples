"""В Python генератор — это обычная функция,
но способная сохранять своё внутреннее состояние.

Синтаксически функция-генератор отличается наличием
оператора yield при достижении которого поток управления
переходит к месту вызова генератора.
"""


def counter(start=1):
    """Генераторная функция бесконечного счётчика.
    """
    i = start
    while True:
        yield i     # Генерация значения
        i += 1


# Использование бесконечного счётчика
print("Бесконечный счётчик")
for i in counter(7):
    if i == 11:
        break
    print(i)

# То же самое можно описать так
print("Бесконечный счётчик hard code")
gen = counter(7)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
# counter — бесконечный счётчик,
# поэтому он не может закончиться (реализоваться)


# Другой пример
def my_range(start, stop, step):
    """Почти аналог стандартного range.
    """
    i = start
    while i < stop:
        yield i
        i += step


print("my_range")
for i in range(3, 7, 2):
    print(i)

# То же самое можно описать так
print("my_range hard code")
range_gen = my_range(3, 7, 2)
print(next(range_gen))
print(next(range_gen))
# Но этот генератор уже конечен. После генерации последнего значения
# генератор реализован и не может использоваться повторно.
# Поэтому при попытке next(range_gen) получим исключение StopIteration
try:
    print(next(range_gen))
except StopIteration:
    print("Генератор range_gen закончился...")
# Таков принцип работы цикла for —
# такой алгоритм называется протоколом итератора


# В модуле itertools полно готовых генераторов
import itertools as iters


print("Комбинации")
combs = iters.combinations([1, 2, 3, 4, 5], r=2)
for pair in combs:
    print(pair)

print("Декартово произведение")
# Свёртка вложенных циклов
for i, j in iters.product(range(3), range(2)):
    print(i, j)
# Аналог
print("Вложенные циклы без декартова произведения")
for i in range(3):
    for j in range(2):
        print(i, j)

# ...и множество других генераторных функций
