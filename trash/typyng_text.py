"""
Печать текста как печатная машинка
В этой версии программа печатает с новой строки строку из массива.
"""
from time import sleep


def type_string(in_str: str) -> None:
    for index in range(len(in_str) + 1):
        print(in_str[:index], end="")
        sleep(0.1)
        print(end="\r")


if __name__ == "__main__":
    test_s = ["Знакома ли вам ситуация, когда программа Python должна выполняться не сразу?",
              "В большинстве случаев требуется, чтобы код запускался как можно скорее.",
              "Однако порой перед работой оптимальнее будет дать программе немного поспать."]
    for st_out in test_s:
        type_string(st_out)
        print()
        