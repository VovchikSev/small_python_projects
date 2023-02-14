# moonlander.py

"""эта игра имитирует посадку лунного посадочного модуля (LM) на Луну. вы пилот, и вам нужно контролировать,
сколько топлива вы сжигаете в ретро-ракетах, чтобы скорость вашего спуска замедлилась до нуля, как только ваша высота
над поверхностью Луны достигнет нуля. Если вы ударяетесь о Луну более чем на 5 м ниже поверхности или ваша скорость
при ударе превышает 5 м / с, то считается, что вы потерпели крушение. В противном случае это считается "хорошей"
посадкой. Если у вас закончится топливо, LLM ускорится к Луне под действием силы тяжести."""

# set up the initial parameters - настройка начальных параметров
speed = 30  # speed approaching the moon # скорость, приближения к Луне
fuel = 1500  # how much fuel is left # сколько топлива осталось
altitude = 1000  # altitude above moon # высота над луной
gravity = 1.622  # acceleration due to gravity # ускорение под действием силы тяжести
burn = 0  # initial rate of burning fuel in retrorockets

# while LLM is above the moon's surface,
# calculate flight data and take input from pilot
while altitude > 0:
    # calculate how long until LLM will impact moon at current speed (impact)
    if speed <= 0:
        impact = 1000
    else:
        impact = altitude / speed
    # display flight data
    print(f"Высота:{altitude:8.3f} Скорость:{speed:6.3f} Топливо:{fuel:8.3f} Влияние:{impact:6.3f} "
          f"Прошлое топливо:{burn:6.3f}")
        # "Altitude={:8.3f} Speed={:6.3f} Fuel={:8.3f} Impact={:6.3f} Previous burn={:6.3f}".
        # format(altitude, speed, fuel,
        #                                                                                           impact, burn))
    # take input from pilot
    # burn = float(input("Enter fuel to burn (0-50)?"))
    burn = float(input("Количество топлива (0-50)?"))

    # ensure rate of fuel burning is within rocket's capability and doesn't exceed remaining fuel
    if burn < 0:
        burn = 0
    if burn > 50:
        burn = 50
    if burn > fuel:
        burn = fuel
    # calculate new flight data
    altitude -= speed
    speed += gravity - burn / 10
    fuel -= burn
# loop has ended, so we must have hit moon's surface
# display final flight data and assess whether it was a crash or a good landing
print("Altitude={:8.3f} Speed={:6.3f} Fuel={:8.3f} Last burn={:6.3f}".format(altitude, speed, fuel, burn))
if altitude < - 5 or speed > 5:
    print("Вы потерпели крушение!")
else:
    print("Вы прилунились удачно!")
