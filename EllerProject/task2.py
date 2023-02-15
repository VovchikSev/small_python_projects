"""
Каждый следующий элемент ряда Фибоначчи получается при сложении двух предыдущих. Начиная с 1 и 2, первые 10 элементов будут:

1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...

Найдите сумму всех четных элементов ряда Фибоначчи, которые не превышают четыре миллиона.
"""

f1, f2, s = 0, 1, 0
while f2 <= 4000000:
    s = s + f2 if f2 % 2 == 0 else s
    f1, f2 = f2, f1 + f2
print(s)