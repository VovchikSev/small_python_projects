# условие: сложить все числа кратные 3 или 5 из чисел меньше 1000
# дано:
"""
# похоже на нормальный метод решения. Результат = 233168
limit = 1000
koefficients = (3, 5)

# решение:
summa = 0
for finded in range(limit):
    for koef in koefficients:
        if finded % koef == 0:
            summa += finded
            break
print(summa)
"""
"""
def compute():
    ans = sum(x for x in range(1000) if (x % 3 == 0 or x % 5 == 0))
    return str(ans)


if __name__ == "__main__":
    print(compute())
"""

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
