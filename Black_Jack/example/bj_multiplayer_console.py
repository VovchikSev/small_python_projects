
# пример с адреса https://www.pyblog.ru/post/pishem_21_na_python_s_multipleerom/
def deckCreate():
    ''' создает колоду карт '''

    suits = ['\u2665', '\u2666', '\u2660', '\u2663']        # unicode символы мастей
    cards = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    all_cards = {j + i for i in suits for j in cards}       # заполнение колоды
    deck = {}
    for card in all_cards:                                  # присваиваем каждой карте очки
        # для карт от 6 до 9 номинал - первый символ
        # для карты 10 номинал первые два символа
        # для картинок J - 2, Q - 3, K - 4, A - 11
        if len(card) == 2:
            if card[0] == 'A':
                deck[card] = 11
            elif card[0] == 'K':
                deck[card] = 4
            elif card[0] == 'Q':
                deck[card] = 3
            elif card[0] == 'J':
                deck[card] = 2
            else:
                deck[card] = card[0]
        else:
            deck[card] = card[:2]

    return deck


def play():
    """ игровой процесс """

    currentPlayer = 'Игрок 1:'
    currentSum = sum1 = sum2 = 0

    hand = ''

    deck = deckCreate()

    while True:
        action = input(currentPlayer + ' Берем карту или хватит? Б-берем, Х-хватит: ')
        if action.lower() == 'б':
            card = deck.popitem()
            currentSum += int(card[1])
            hand += card[0] + ' '
            print(currentPlayer, hand, 'Сумма очков = ' + str(currentSum))

            if currentSum > 21:
                print('Поражение ' + currentPlayer)
                break
            elif currentSum == 21:
                print('Победа ' + currentPlayer)
                break

        # переход хода к другом игроку или конец игры
        if action.lower() == 'х':
            if currentPlayer != 'Игрок 2:':
                sum1 = currentSum
                currentSum = 0
                hand = ''
                currentPlayer = 'Игрок 2:'
            else:
                sum2 = currentSum
                if sum1 > sum2:
                    print('Победа' + 'Игрок 1')
                elif sum1 < sum2:
                    print('Победа' + 'Игрок 2')
                else:
                    print('Ничья')
                break

play()