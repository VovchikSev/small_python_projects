"""
По мотивам https://www.youtube.com/watch?v=ccf1t5EEC_M (первое видео)
Проект приостановлен на видео № 6 https://www.youtube.com/watch?v=f-b2rgNIUz8 30я минута.
Перенос всех проектов в одну общую среду в одну папку.

Test Drive Development - TDD
Adventure game тип симулятор ходьбы.
Плоский мир на котором могут быть объекты типа: дерево, камень, клад, инструкция, монстр.
Игрок располагается в центре карты.
Радиус обзора 4Х4 от позиции игрока.
Игрок может идти по пустым ячейкам.
Может рубить дерево, на месте срубленного дерева остаётся пустая ячейка.
Может читать инструкцию. После прочтения она заменяется на пустую ячейку.
Может подобрать в инвентарь клад.
Может сражаться с монстром. (монстр из другого урока).
Может убежать от монстра, монстр неподвижен, пока.
Не может пройти камень.

Цель игры: собрать все сокровища на карте.

w, s, a, d - движение по карте
i - собрать в инвентарь.
r - читать инструкцию.
x - рубить дерево.
f - атаковать соседнего монстра.

Как выглядит проект со стороны игрока:
..........................
.  @         1           .
. *   1  x   $           .
..........................
"В вашем инвентаре 0 сокровищ"
"Ваше действие [w, s, a, d]:?"
При выводе возможных действий исключать букву направления в сторону преграды.
"""
"""
Цикл разработки с TDD
1. Красный тест: Пишем тест который выполнится с ошибкой. Тест на несуществующий функционал.
2. Зеленый тест: Максимально простым способом заставляем функционал выполнятся.
3. Рефакторинг.

Не знаешь с чего начать, начинай с теста!
"""
from src.options import *
from src.game import Game

game = Game()


game.run()
