# Tom Baker
# Lander 2
# Main program

import pygame
import random
import time
import os

# Define some constant colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Define the game screen and win/lose messages.
pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
SIZE = (900, 600)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Lander 2")
font = pygame.font.SysFont("Calibri", 30, True, False)
small_font = pygame.font.SysFont("Calibri", 20, True, False)
fuel_bar = small_font.render("Fuel", True, GREEN)
win = font.render("You landed safely!", True, WHITE)
crash_landing = font.render("You hit the ground too hard!", True, WHITE)
crash = font.render("You didn't manage to land correctly.", True, WHITE)
disappear = font.render("You float away and are never heard from again.", True, WHITE)
death = font.render("Game over!", True, WHITE)
lives = 3
died = False
# Defines clock for screen refreshing.
CLOCK = pygame.time.Clock()


def start():
    global player, ground, done, won, crashed, crash_landed, disappeared
    ground = Ground()
    player = Ship()
    done = False
    won = False
    crashed = False
    crash_landed = False
    disappeared = False
    main()


class Ground():

    def __init__(self):
        self.length = random.randint(22, 200)
        self.x_coord = random.randint(0, 900 - self.length)
        self.y_coord = random.randint(500, 570)


class Ship():

    def __init__(self):
        self.max_fuel = (200 - ground.length) * 2.5
        self.fuel = self.max_fuel
        self.x_coord = random.randint(1, 879)
        self.y_coord = 200
        self.left_speed = 0
        self.right_speed = 0
        self.fall_speed = 0
        self.fuel_warning = GREEN
        self.move_left = False
        self.move_right = False
        self.falling = True


def main():
    global BLACK, WHITE, BLUE, GREEN, done, won, crashed, crash_landed, disappeared, lives, died
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_left = False
                if event.key == pygame.K_RIGHT:
                    player.move_right = False
                if event.key == pygame.K_SPACE:
                    player.falling = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT:
                    player.move_left = True
                if event.key == pygame.K_RIGHT:
                    player.move_right = True
                if event.key == pygame.K_SPACE and player.fuel > 0:
                    player.falling = False

        # GAME LOGIC
        # If the game is over, restart the game.
        if died:
            time.sleep(2)
            pygame.quit()
        if won or crashed or crash_landed or disappeared:
            time.sleep(2)
            start()
        # If keys are pressed.
        if player.move_left:
            player.left_speed -= .02
            if player.left_speed < -5:
                player.left_speed = -5
        if player.move_right:
            player.right_speed += .02
            if player.right_speed > 5:
                player.right_speed = 5
        if not player.falling and player.fuel > 0:
            player.fuel -= 1
            if player.fuel < player.max_fuel * .2:
                player.fuel_warning = RED
            if player.fuel < 0:
                player.fuel = 0
            player.fall_speed -= .02
            if player.fall_speed < -5:
                player.fall_speed = -5
        # If keys are not pressed.
        if not player.move_left:
            player.left_speed += .01
            if player.left_speed > 0:
                player.left_speed = 0
        if not player.move_right:
            player.right_speed -= .01
            if player.right_speed < 0:
                player.right_speed = 0
        if player.falling or player.fuel < 1:
            player.fall_speed += .01
            if player.fall_speed > 5:
                player.fall_speed = 5
        # Check if player landed on the ground or crashed
        player_ship = pygame.Rect(player.x_coord, player.y_coord, 19, 25)
        landing_area = pygame.Rect(ground.x_coord, ground.y_coord - 28, ground.length, 28)
        ground_rect = pygame.Rect(ground.x_coord, ground.y_coord, ground.length, 30)
        if landing_area.contains(player_ship) and round(player.y_coord + 20, 0) <= ground.y_coord:
            if player.fall_speed < 1.5:
                won = True
            else:
                crash_landed = True
            player.fall_speed = 0
        if player_ship.colliderect(ground_rect) and round(player.y_coord + 20, 0) > ground.y_coord:
            crashed = True
            player.fall_speed = 0
        if True:
            # Calculate player coordinates and keep them on the screen.
            player.x_coord = player.x_coord + player.left_speed + player.right_speed
            player.y_coord += player.fall_speed
            if player.x_coord > 880:
                player.x_coord = 880
                player.left_speed = 0
                player.right_speed = 0
            if player.x_coord < 0:
                player.x_coord = 0
                player.left_speed = 0
                player.right_speed = 0
            if player.y_coord > 600:
                player.y_coord = 600
                disappeared = True
                player.fall_speed = 0

            # DRAWING CODE.
            screen.fill(BLACK)
            # Draw win/lose text.
            if crashed or crash_landed or disappeared:
                lives -= 1
                if lives < 1:
                    died = True
            if won and not died:
                screen.blit(win, [335, 250])
            if crashed and not died:
                screen.blit(crash, [230, 250])
            if crash_landed and not died:
                screen.blit(crash_landing, [270, 250])
            if disappeared and not died:
                screen.blit(disappear, [155, 250])
            if died:
                screen.blit(death, [370, 250])
            # Draw the lander engine fire.
            if not player.falling:
                pygame.draw.line(screen, RED, [player.x_coord + 7, player.y_coord + 15],
                                 [player.x_coord + 10, player.y_coord + 25], 2)
                pygame.draw.line(screen, RED, [player.x_coord + 13, player.y_coord + 15],
                                 [player.x_coord + 10, player.y_coord + 25], 2)
            # Draw the lander.
            pygame.draw.ellipse(screen, WHITE, [player.x_coord, player.y_coord, 20, 12], 1)
            pygame.draw.rect(screen, WHITE, [player.x_coord, player.y_coord + 10, 20, 5], 1)
            pygame.draw.line(screen, WHITE, [player.x_coord + 2, player.y_coord + 5],
                             [player.x_coord, player.y_coord + 25], 1)
            pygame.draw.line(screen, WHITE, [player.x_coord + 17, player.y_coord + 5],
                             [player.x_coord + 19, player.y_coord + 25], 1)
            # Draw the fuel level bar.
            screen.blit(fuel_bar, [432, 5])
            pygame.draw.line(screen, player.fuel_warning, [450 - player.fuel / 2, 30],
                             [450 + player.fuel / 2, 30], 5)
            # Draw the lives display.
            lives_display = font.render("Lives: " + str(lives), True, GREEN)
            screen.blit(lives_display, [0, 0])
            # Draw the ground.
            pygame.draw.rect(screen, BLUE, [ground.x_coord, ground.y_coord, ground.length, 30])
            # Update the screen.
            pygame.display.flip()
            CLOCK.tick(60)
    pygame.quit()

# Make a new ship and start the game.
start()
