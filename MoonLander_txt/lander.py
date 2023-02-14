"""Программа симуляции посадки.
Использует объект типа moon_lander.py
"""
from ship_data import Ship


def main():
    my_ship = Ship()
    while my_ship.altitude > 0:
        print(f"Высота:{my_ship.altitude:6.3f} Скорость: {my_ship.speed:6.3f} Топливо: {my_ship.fuel:6.3f} "
              f"Влияние: {my_ship.impact:6.3f} Прошлое топливо:{my_ship.burn:6.3f}")
        my_ship.set_burn(input("Количество топлива (0-50)?"))


main()
