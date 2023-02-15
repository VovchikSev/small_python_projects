
# Если выписать все натуральные числа меньше 10, кратные 3 или 5, то получим 3, 5, 6 и 9. Сумма этих чисел равна 23.

# Найдите сумму всех чисел меньше 1000, кратных 3 или 5.
"""
это ни что иное как многострочный комментарий.
"""


def compute():
    ans = sum(x for x in range(1000) if (x % 3 == 0 or x % 5 == 0))
    return str(ans)


if __name__ == "__main__":
    print(compute())


def com():
    numbers = []
    for i in range(0, 1000):
        if (i % 3) == 0:
            numbers.append(i)
        elif (i % 5) == 0:
            numbers.append(i)
            a = sum(numbers)
    return a


print(com())
