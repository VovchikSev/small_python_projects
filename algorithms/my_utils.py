

def generate_random_list(start: int = -100, finish: int = 100, list_len: int = 10) -> list:
    """
    :param start: Начало диапазона для выбора случайных чисел, по умолчанию -100
    :param finish: Конец диапазона для выбора случайных чисел, по умолчанию 100.
    :param list_len: Количество случайных чисел в списке, по умолчанию 10.
    :return: несортированный список случайных чисел в диапазоне от start до finish длинной list_len
    """
    import random
    lst = []
    while len(lst) < list_len:
        random_value = random.randint(start, finish)
        if random_value not in lst:
            lst.append(random_value)
    return lst


if __name__ == '__main__':
    pass
