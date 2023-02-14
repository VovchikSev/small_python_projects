
# очко Black Jack по умному
# тест колод
# колоды использовать на 52 карты без джокеров
# koloda = [6,7,8,9,10,2,3,4,11] * 4
# import random
# random.shuffle(koloda)
# print(koloda)
# очень примитивно, вот получше
import random
import itertools

# переделать на получение из списков без модуля itertools
SUITS = 'cdhs'  # масти
RANKS = '23456789TJQKA'  # достоинства
# создание списка колоды карт
DECK = list(''.join(card) for card in itertools.product(RANKS, SUITS))
# получение случайных карт, но колода не задействована
hand = random.sample(DECK, 5)

print(hand)
print(DECK)

random.shuffle(DECK)  # перемешанная колода.
print(len(DECK))
print(DECK)  # отобразить перемешанную колоду
# получить из колоды 5 карт
for _ in range(5):
    print(DECK.pop(0), end=" ")
# отобразить остаток колоды
print(len(DECK))
print(DECK)
# ['Kh', 'Kc', '6c', '7d', '3d']

