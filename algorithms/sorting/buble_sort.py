# сгенерировать список из х чисел в диапазоне от -100 до 100
from my_utils import generate_random_list


def bubble_sorting(in_lst: list) -> list:
    for a_index in range(len(in_lst) - 1):
        for b_index in range(len(in_lst) - 1 - a_index):
            if in_lst[b_index] > in_lst[b_index + 1]:
                in_lst[b_index], in_lst[b_index + 1] = in_lst[b_index + 1], in_lst[b_index]
        
    return in_lst
    
    
if __name__ == '__main__':
    x = 10 # количество сортируемых элементов
    lst = [-89, 52, -69, 92, 66, 83, -5, -84, -52, -49]
    # lst = generate_random_list(list_len=x, start= -99, finish=99)  # сортируемый список
    # заполнение массива lst случайными значениями
    
    print(lst.copy())
    print(bubble_sorting(eval(str(lst))))