
# сгенерировать список из х чисел в диапазоне от -100 до 100
from my_utils import generate_random_list


def selection_sort_one_cycle(p_lst:list) -> list:
    for a_index in range(len(p_lst) - 1):
        # найти наименьшее и поменять местами со значением lst[a_index] с найденным минимальным значением
        min_index = p_lst.index(min(p_lst[a_index + 1::]), a_index + 1, len(p_lst))
        if p_lst[a_index] > p_lst[min_index]:
            p_lst[a_index], p_lst[min_index] = p_lst[min_index], p_lst[a_index]
    return p_lst


def selection_sort_two_cycle(p_lst: list) -> list:
    for a_index in range(len(p_lst) - 1):
        min_index = a_index
        for b_index in range(a_index + 1, len(p_lst)):
            if p_lst[b_index] < p_lst[min_index]:
                min_index = b_index
                
        if p_lst[a_index] > p_lst[min_index]:
            p_lst[a_index], p_lst[min_index] = p_lst[min_index], p_lst[a_index]
            
    return p_lst


x = 10
lst = generate_random_list()
print(lst)

print(selection_sort_two_cycle(eval(str(lst))))

