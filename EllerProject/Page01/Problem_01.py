"""
01
https://projecteuler.net/problem=1
Если выписать все натуральные числа меньше 10, кратные 3 или 5, то получим 3, 5, 6 и 9.
Сумма этих чисел равна 23.
Найдите сумму всех чисел меньше 1000, кратных 3 или 5.
"""


def main():
    my_sum = 0
    for ch in range(1000):
        if ch % 3 == 0 or 0 == ch % 5:
            # print(ch)
            my_sum += ch
    print(my_sum)


if __name__ == "__main__":
    main()
