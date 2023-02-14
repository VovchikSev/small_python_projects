# интересно, требует подробного разбора.
import random
from time import sleep

player_victory = 0
computer_victory = 0

n = 1

detect = {'6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 2, 'Q': 3, 'K': 4}

print('Игра "Блэк Джэк"\n')

while True:
    print(f'Раунд {n}-й\n')

    # Инициализация нового раунда
    player_cards = []
    player_sum = 0

    computer_cards = []
    computer_sum = 0

    cards = [(mast, numb) for mast in range(4) for numb in ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
    random.shuffle(cards)

    # Раздача карт
    player_cards.append(cards.pop())
    player_cards.append(cards.pop())
    for mast, numb in player_cards:
        if numb == 'A':
            if player_sum + 11 > 21:
                player_sum += 1
            else:
                player_sum += 11
        else:
            player_sum += detect[numb]

    computer_cards.append(cards.pop())
    computer_cards.append(cards.pop())
    for mast, numb in computer_cards:
        if numb == 'A':
            if computer_sum + 11 > 21:
                computer_sum += 1
            else:
                computer_sum += 11
        else:
            computer_sum += detect[numb]

    # Ход игрока
    while True:
        print('Ваши карты: ', end='')
        for mast, numb in player_cards:
            print(numb, ['червы', 'бубны', 'трефы', 'пики'][mast], end='; ')

        print(f'\nСумма очков: {player_sum}')

        if player_sum > 21:
            sleep(2)
            break

        cmd = input('Взять еще одну карту? (y/n) > ')
        if cmd == 'n' or cmd == 'N':
            break
        elif cmd == 'y' or cmd == 'Y':
            card = cards.pop()
            numb = card[1]
            player_cards.append(card)

            if numb == 'A':
                if player_sum + 11 > 21:
                    player_sum += 1
                else:
                    player_sum += 11
            else:
                player_sum += detect[numb]

        print()

    # Ход компьютера
    while True:
        if computer_sum + 5 <= 21:
            card = cards.pop()
            numb = card[1]
            computer_cards.append(card)

            if numb == 'A':
                if computer_sum + 11 > 21:
                    computer_sum += 1
                else:
                    computer_sum += 11
            else:
                computer_sum += detect[numb]
        else:
            break

    print('\nКарты компьютера: ', end='')
    for mast, numb in computer_cards:
        print(numb, ['червы', 'бубны', 'трефы', 'пики'][mast], end='; ')

    print(f'\nСумма очков компьютера: {computer_sum}')

    if (player_sum == computer_sum) or (computer_sum > 21 and player_sum > 21):
        print('\nНичья\n')
        n += 1
        sleep(5)
    elif player_sum > 21 or (player_sum < computer_sum and computer_sum < 22):
        print('\nВ этом раунде победил компьютер\n')
        computer_victory += 1
        n += 1
        sleep(5)
    else:
        print('\nВ этом раунде победил человек\n')
        player_victory += 1
        n += 1
        sleep(5)

    if player_victory == 5:
        print('\nПобедитель: человек!')
        break

    if computer_victory == 5:
        print('\nПобедитель: компьютер!')
        break