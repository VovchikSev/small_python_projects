import pygame

from random import randint, uniform, choice
from math import sin, cos, radians
from datetime import datetime
from os import listdir


# Lander class contains the ship and all of its properties
class Lander:
    def __init__(self, lives, fuel, score, screen, damage=0):
        # lander 'object'
        self.lander = load_image("Resources/lander.png")
        # static image of lander, used to calculate rotation
        self.lander_img = self.lander.copy()
        # thrust 'object'
        self.lander_thrust = load_image("Resources/thrust.png")
        # static thrust image used to calculate rotation
        self.lander_thrust_img = self.lander_thrust.copy()

        # gravity expressed in (m/s^2 / 10) //Earth's gravity would be 0.981 in this case
        self.g = 0.371

        # seconds
        self.control_disable_time = 2
        # holds values of controls and disabled time
        #   0th index = control, 1st index = time
        #       0 = working
        #       1 = temporarily disabled (2 seconds as requirements say)
        #       2 = broken (disabled until a new ship is deployed, in this case losing a life)
        self.controls = [[0, 0], [0, 0], [0, 0]]

        # spawn location of lander and random X-axis velocity
        self.x = randint(0, screen.get_width()-self.lander.get_width())
        self.x_velocity = uniform(-5, 5)
        self.y = randint(0, self.lander.get_height()*4)
        self.y_velocity = 0

        # angle of lander and its box
        self.angle = 0
        self.rect = self.lander.get_rect()

        # fuel of lander
        self.fuel = fuel
        # remaining lives of the pilot (i guess?)
        self.lives = lives
        # score
        self.score = score

        # damage taken by lander
        self.damage = damage

    # update_lander re-calculates the position of the ship, taking into consideration user input and game physics
    def update_lander(self, screen, tick_rate):
        # world constrictions
        def constrict_lander(lander, x, y, scr):
            # x, y are lander's location,
            # lander is essentially self, passed it just in case
            # scr is game.screen, kept it as scr due to Pycharm warnings
            if y < 0:
                # if lander is above screen, upwards speed to 0 and set y-axis to 0
                y = 0
                lander.y_velocity = 0

            # if lander reaches the ground of the planet, it crashes and restarts the game
            elif y > scr.get_height():
                # notification that lets know what happened
                game.pause("YOU HAVE CRASHED INTO THE GROUND", any_key=1, small=1)
                # consequences of the crash and value reset
                lander.lives -= 1
                lander.damage = 0
                # fuel is usually passed down as I wanted to remove the possibility of an infinite game.
                lander.fuel = 500
                game.restart(lander)

            # if the ship goes to the right beyond the screen, it gets moved back to the far left
            # we remove the width of the ship due to the nature of how py-game visualises images
            if x > scr.get_width() - lander.lander.get_width():
                x = 0
            # vice versa
            elif x < 0:
                x = scr.get_width() - lander.lander.get_width()

            return x, y

        # calls for the lander's physics
        self.gravity()

        # makes sure the lander locations are within accepted range
        self.x, self.y = constrict_lander(self, self.x, self.y, screen)

        # updates the hit box of the ship
        self.rect = self.lander.get_rect()

        # visualizes the ship
        screen.blit(self.lander, (self.x, self.y))

        # iterates through our controls
        for control in self.controls:
            # if control is temporarily disabled
            if control[0] == 1:
                # fraction of a second (f_sec) is 1second/tick rate (in this case 30)
                f_sec = 1/tick_rate
                # if the time left on the temporary disable is more than 0,
                if control[1] > 0:
                    # reduce the time by 1/30 seconds, every time the game ticks
                    control[1] -= f_sec
                # else if time left is less than 0, set the control attribute and time to 0
                if control[1] < 0:
                    control[0] = 0
                    control[1] = 0

    # ship's gravitational pull
    def gravity(self):
        # balance is an issue, so far these are the numbers I found work 'best'
        # checks if velocity is 'negative' (left) or 'positive' (right)
        # gravity forces the x_velocity to be reduced by 0.01 every 3 ticks roughly, these are the best numbers I found
        if self.x_velocity < 0:
            self.x_velocity += self.g / 100

        elif self.x_velocity > 0:
            self.x_velocity -= self.g / 100

        # increases the downwards velocity by 0.371/30 per tick
        self.y_velocity += self.g/30
        self.x += self.x_velocity
        self.y += self.y_velocity

    # this spends fuel in order move the ship in the direction opposite of its legs
    def thrust(self, screen):
        # if we have fuel and our systems are working
        if self.fuel > 1 and self.controls[1][0] == 0:
            # convert the angle of the lander into a functional angle in the range (0, 360), we add 90 to
            # simulate 90 degree angle being the upwards position of lander (nose pointing up)
            angle = radians((self.angle + 90) % 360)

            # where 0.33 was recommended, I found it too fast for my build of the game, changed it to 0.2
            self.x_velocity += 0.2 * cos(angle)
            self.y_velocity += -0.2 * sin(angle)

            # reduce fuel by 5
            self.fuel -= 5

            # half height and width of the lander (radius)
            w = self.lander.get_width() / 2
            h = self.lander.get_height() / 2
            # I know I need the location of the "bottom" of the ship in
            # order to calculate it but I could not figure out how, found these numbers to work best
            x = self.x + (w - w * cos(angle))
            # without the -10, the flame was getting too far away
            y = self.y + (h-10 + h * sin(angle))

            # visualizes our thrust flame
            screen.blit(self.lander_thrust, (x, y))

    # rotates the ship by 3 degrees per tick if held down (-1 left, 0 none, 1 right)
    def rotate(self, direction=0):
        # if the direction is left and the left wing is not broken
        if direction == -1 and self.controls[0][0] == 0:
            # rotate by 3 degrees
            self.angle += 3
        # if the direction is right and the right wing is not broken
        elif direction == 1 and self.controls[2][0] == 0:
            # rotate by 3 degrees
            self.angle -= 3
        # hit box of the lander
        self.rect = self.lander.get_rect().center

        # lander gets replaced with a rotated version of the stock lander image (avoids reusing a distorted image)
        self.lander = pygame.transform.rotozoom(self.lander_img, self.angle, 1)
        # helps avoid image distortion on rotation
        self.lander.get_rect().center = self.rect
        # rotates the thrust (even though it's invisible)
        self.lander_thrust = pygame.transform.rotozoom(self.lander_thrust_img, self.angle, 1)

    # self explanatory, breaks a random control for 2.0 seconds
    def control_failure(self):
        # random part index
        i = randint(0, len(self.controls)-1)
        # helps making things clearer as to how this method works
        part, time = 0, 1
        # short-cut
        disabled_time = self.control_disable_time

        # if the part is functioning
        if self.controls[i][part] == 0:
            # break it for 2.0s
            self.controls[i] = [1, disabled_time]

        # checks if current part is temporarily disabled
        elif self.controls[i][part] == 1:
            # checks all parts to see if there's a functioning one in order to randomly damage
            for p, t in self.controls:
                # if there exists a part that functions
                if p == 0:
                    # calls back the control_failure method -> generates new random part and repeats
                    self.control_failure()

        # if the part is 'permanently' disabled/has taken major damage, nothing can fix it, for now

    # checks if the ship has landed (touched a pad)
    def is_landed(self, pads):
        # hit box of lander
        self.rect = self.lander.get_rect()
        # hit box gets x and y added to it
        self.rect[0] = self.x
        self.rect[1] = self.y
        # iterates all of the pads
        for pad, xy in pads:
            # hit box of pad
            pad_rect = pad.get_rect()
            # hit box gets x and y added to it
            pad_rect[0] = xy[0]
            pad_rect[1] = xy[1]
            # if the hit box of the lander contacts the hit box of a pad
            if self.rect.colliderect(pad_rect):
                # check the type of contact between the two
                self.landing_type(pad_rect)

    # checks what kind of a landing it is (proper feet placement, speed, location etc.)
    def landing_type(self, pad_rect):
        # short-cuts for lander's speeds
        vel_x = abs(self.x_velocity)
        vel_y = abs(self.y_velocity)

        # pad_x and pad_w are the x location and width of the pad that is touched
        pad_x, _, pad_w, _ = pad_rect
        # width of the lander's hit box
        w = self.lander.get_width()

        # add 90 degrees to lander's angle so that when angle is 90, the lander is pointing up
        angle = (self.angle+90) % 360
        # range of accepted by the game landing angles
        good_angles = range(85, 95)
        # boolean = lander's angle is not in-between 85 and 95
        bad_angle = angle not in good_angles

        # boolean = velocities are above 2.5
        too_fast = (vel_x >= 2.5 or vel_y >= 2.5)

        # pad_s is the x coordinate where the hit box starts, pad_f is the x coordinate where the hit box ends
        pad_s, pad_f = pad_x, (pad_x+pad_w-w)
        bad_placement = not(int(self.x) in range(pad_s, pad_f))

        # self explanatory if
        if bad_angle or too_fast or bad_placement:
            # if we 'land' improperly, we crash into the pad
            self.damage = 100
            # notification w/ pause
            game.pause("YOU HAVE CRASHED INTO A PAD", any_key=1, small=1)
            # lose a life and get passed down attributes reset
            self.lives -= 1
            self.damage = 0
            self.fuel = 500
        else:
            # successful landing, get 50 score and a notification w/ a pause
            self.score += 50
            game.pause("SUCCESSFUL LANDING", any_key=1, small=1)

        # restart the game
        game.restart(self)

    # triggered whenever it collides with an obstacle or meteor
    def is_damaged(self, obstacle, meteor):
        # this function turned out to be quite messy, obstacle and meteor are in the environment class
        # hit box of lander
        self.rect = self.lander.get_rect()
        # add x and y to hit box
        self.rect[0] = self.x
        self.rect[1] = self.y

        # this is a short-cut to the the list of obstacles and their hit boxes
        obstacles = obstacle.obstacles
        # this is a short-cut to the the list of meteors and their hit boxes
        meteors = meteor.meteors

        # checks if the ship has taken too much damage, if yes then it restarts the game
        if self.damage >= 100:
            # if damage goes beyond 100, set it back to 100 for aesthetic purposes
            self.damage = 100
            # if for some reason we're still going upwards, get our upwards velocity null'd out so the ship goes down
            if self.y_velocity < 0:
                # replace the upwards velocity with a downwards velocity of 1
                self.y_velocity = 1
            # disable all controls if damage is 100
            self.controls = [[2, 0] for _ in range(len(self.controls))]

        # iterates through all obstacles
        for obs, loc in obstacles:
            # checks if the ship collides with any of the obstacles
            if self.rect.colliderect(loc):
                # the index of the obstacle that has collided with the ship
                i = obstacle.obstacles.index([obs, loc])
                # removes obstacle that the player has crashed into
                obstacle.destroy_obstacle(i)
                # if our damage is below 100%
                if self.damage < 100:
                    # reduce velocities by 10%
                    self.x_velocity *= 0.9
                    self.y_velocity *= 0.9
                    # add 10% damage
                    self.damage += 10
                # if our damage is above 100%
                else:
                    # increase y velocity by 10% (speeds up, user waits less to fall down)
                    # add a random x_vel to make crash process faster
                    self.x_velocity += randint(-2, 2)
                    self.y_velocity *= 1.1

        # iterates through all meteors
        for met, loc, vel in meteors:
            # if a meteor collides with the ship
            if self.rect.colliderect(loc):
                # index of the meteor that has collided with the ship
                i = meteors.index([met, loc, vel])
                # destroy the collided meteor
                meteor.destroy_meteor(i)
                # if ship damage is under 100
                if self.damage < 100:
                    # decrease ship velocity by 25%
                    self.x_velocity *= 0.75
                    self.y_velocity *= 0.75
                    # increase ship damage by 25%
                    self.damage += 25
                else:
                    # increase y velocity by 25% (speeds up, user waits less to fall down)
                    # add a random x_vel to make crash process faster
                    self.x_velocity += randint(-2, 2)
                    self.y_velocity *= 1.25


# Environment class contains the pad, obstacle and meteor classes, keeps tab of all non-lander game objects
class Environment:
    # I honestly have no clue what I was thinking when I was making this class as it's far from good OOP

    # Pad class contains the random pads
    class Pad:
        def __init__(self, screen, amount):
            # all pad images
            self.pad_images = listdir("Resources/landingPads")
            # amount of required pads
            self.amount = amount
            # pad container, this is not the best way of doing it and I later realised it, described in the end
            self.pads = []
            # hit box of a pad
            self.rect = None
            # game screen
            self.screen = screen

            # calls the creation of pads
            self.create_pad()

        def create_pad(self):
            # width and height of the screen
            w = self.screen.get_width()
            h = self.screen.get_height()

            # creates "slots" for the pads on the game screen, depends on the game screen width and number of pads
            slot_width = int(w / self.amount)

            for i in range(self.amount):
                # chooses random types of pads which will later define pad location
                rand_pad_image = choice(self.pad_images)
                pad = load_image("Resources/landingPads/" + rand_pad_image)

                # creates an index and "slot" for the pad in the list
                self.pads.append(pad)

                # s,f are 'indexes' which define a slot by the slot_width
                # (e.g. if 4 pads, (0*400, 1*400), (1*400, 2*400) etc.)
                s, f = i, i+1

                # random x location for a pad, 158 is the width of the pad
                pad_x = randint(s*slot_width, f*slot_width-158)

                # assuming pad is of the floating type, assumption saves lines
                pad_y = h-randint(200, 400)

                # checks if the pad type has legs
                if "x82x" in str(self.pads[i]):
                    pad_y = h-randint(10, 82)

                # replaces the pad entry with a list of the pad and its location in the self.pads list
                self.pads[i] = [pad, (pad_x, pad_y)]

    # Meteor class contains the random meteors
    class Meteor:
        def __init__(self, screen, amount):
            # all meteor images in that dir
            self.meteor_images = listdir("Resources/meteors")
            # the list of meteors
            self.meteors = []
            # number of meteors to be spawned on each wave, usually should be a random number each wave
            self.amount = amount
            # game screen
            self.screen = screen

        # creates the meteors
        def create_meteors(self):
            # width and height of the game screen
            _, _, w, h = self.screen.get_rect()

            # iterates through the creation code self.amount times
            for _ in range(self.amount):
                # chooses a random image from the meteors folder
                rand_meteor = choice(self.meteor_images)

                # scale is the size index of the meteors:
                # 1 - biggest meteor; 2 - smaller than 1; 3 - smaller than 2;.. etc.
                scale = self.meteor_images.index(rand_meteor) + 1

                # creates a meteor py-game.surface
                meteor = load_image("Resources/meteors/" + rand_meteor)

                # hit box of the meteor
                rect = meteor.get_rect()

                # meteor width and height
                _, _, mw, mh = rect

                # random x and y coordinates of the meteor such that they always spawn off of the screen
                xy = [randint(-mw*2, w+mw*2), randint(-mh*4, -mh*2)]
                rect[0] = xy[0]
                rect[1] = xy[1]

                # random x and y velocity, per meteor
                x_vel = uniform(0.5, 1.5)
                y_vel = uniform(1, 4)

                # if meteor spawns in the first half of the screen in relativity to the y-axis
                if xy[0] >= w/2:
                    # change it's velocity direction
                    x_vel = -x_vel

                # velocity of the meteors is scaled with their size scale as previously described
                velocity = (round(x_vel*scale, 2), round(y_vel*scale, 2))

                # adds the meteor to the meteors list, again this is not the best way, I've explained it at the
                # very bottom of the source code in a '''comment'''
                self.meteors.append([meteor, rect, velocity])

        # moves a meteor
        def move_meteor(self, i):
            # gets the velocity of the meteor
            x_vel, y_vel = self.meteors[i][2]
            # adds the velocities to the corresponding axis of the meteor
            self.meteors[i][1][0] += x_vel
            self.meteors[i][1][1] += y_vel

            # if the meteor has hit the ground, destroy it
            if self.meteors[i][1][1] >= self.screen.get_height():
                self.destroy_meteor(i)

        # removes/destroys a meteor
        def destroy_meteor(self, i):
            self.meteors.remove(self.meteors[i])

    # Obstacle class contains the random obstacles
    class Obstacle:
        def __init__(self, screen, amount):
            self.obstacle_images = listdir("Resources/obstacles/")

            # number of objects to be created, usually should be a random number
            self.amount = amount
            # the list of obstacles
            self.obstacles = []
            # game screen
            self.screen = screen

            # calls the create_obstacles function
            self.create_obstacles()

        # creates the obstacles used in environment
        def create_obstacles(self):
            # screen width and height
            _, _, w, h = self.screen.get_rect()

            for _ in range(self.amount):
                obstacle = load_image("Resources/obstacles/" + choice(self.obstacle_images))
                # obstacle hit box
                obs_rect = obstacle.get_rect()
                # the width and height of the obstacle
                _, _, ow, oh = obs_rect

                # random x and y coordinates of the obstacle, such that the obstacles can cover:
                # x = entire width of the screen
                # y = entire bottom half of the screen
                xy = [randint(0, w-ow), randint(h/2, h-oh)]

                # sets the x and y in the obstacle's hit box
                obs_rect[0] = xy[0]
                obs_rect[1] = xy[1]

                # random scale, makes things more fun
                scale = randint(60, 100)/100
                # re-sizes the obstacle based on the random scale
                obstacle = pygame.transform.scale(obstacle, (int(ow*scale), int(oh*scale)))

                # adds the obstacle to the obstacles list
                self.obstacles.append([obstacle, obs_rect])

        # destroy an obstacle
        def destroy_obstacle(self, i):
            self.obstacles.remove(self.obstacles[i])

    def __init__(self, screen, pads_amount, obstacle_amount, meteor_amount):
        # game screen
        self.screen = screen
        # we create pad, meteor and obstacle in order to be able to refresh the contents of the classes
        self.pad = self.Pad(self.screen, pads_amount)
        self.meteor = self.Meteor(self.screen, meteor_amount)
        self.obstacle = self.Obstacle(self.screen, obstacle_amount)

    # Adds the environment ot the game screen
    def update_environment(self):
        pads = self.pad.pads
        obstacles = self.obstacle.obstacles
        meteors = self.meteor.meteors

        # iterates through all pads
        for pad, location in pads:
            # visualizes them
            self.screen.blit(pad, location)

        # iterates through all obstacles
        for obstacle, location in obstacles:
            # visualizes them
            self.screen.blit(obstacle, location)

        # iterates through all meteors
        for meteor, location, velocity in meteors:
            # index of iterated through meteor
            i = meteors.index([meteor, location, velocity])
            # moves the meteor with its individual velocities and updates its location
            self.meteor.move_meteor(i)
            # visualizes said meteor
            self.screen.blit(meteor, location)

        # calls for environment interactions
        self.environment_interaction()

    # checks if objects in the environment are interacting
    def environment_interaction(self):
        pads = self.pad.pads
        obstacles = self.obstacle.obstacles
        meteors = self.meteor.meteors

        # iterates through all pads
        for pad, p_location in pads:
            # iterates through all meteors
            for meteor, m_location, velocity in meteors:
                # get pad hit box
                p_rect = pad.get_rect()
                # sets pad hit box x, y location
                p_rect[0] = p_location[0]
                p_rect[1] = p_location[1]
                # if a meteor collides with a pad
                if m_location.colliderect(p_rect):
                    # index of the meteor that has collided with the pad in the meteors list
                    i = meteors.index([meteor, m_location, velocity])
                    # remove that meteor
                    self.meteor.destroy_meteor(i)

        # iterates through all obstacles
        for obstacle, o_location in obstacles:
            # iterates through all meteors
            for meteor, m_location, velocity in meteors:
                # if a meteor collides with an obstacle
                if m_location.colliderect(o_location):
                    # index of meteor in meteors list
                    i = meteors.index([meteor, m_location, velocity])
                    # remove meteor
                    self.meteor.destroy_meteor(i)
                    # index of obstacle in obstacles list
                    i = obstacles.index([obstacle, o_location])
                    # remove obstacle
                    self.obstacle.destroy_obstacle(i)


# Stats class contains the Lander's stats (velocity, latitude etc..). But it's a bit too complex to be kept in Lander
class Stats:
    def __init__(self, scale):
        # starts py-game's font option
        pygame.font.init()
        # all of these hold the same name as the lander stats as they will represent them in a py-game.surface
        self.x_velocity = None
        self.y_velocity = None
        self.damage = None
        self.time = None
        self.fuel = None
        self.altitude = None
        self.score = None
        self.controls = None
        # messages used for the controls' status
        self.controls_messages = ["LEFT WING - ", "ENGINE - ", "RIGHT WING - "]
        # ui scale set by the options in the bottom of the code (where the run is)
        self.scale = scale / 100

        # a box that will hold the surface versions of the lander's attributes
        self.instruments_background = pygame.Surface((480, 215), pygame.SRCALPHA)
        # a 50% transparent black color
        black_t = (0, 0, 0, 127)
        # fill the box with the 50% transparent black color
        self.instruments_background.fill(black_t)

        # color shift is just an integer that gets added per tick to allow for a flashing effect on the text
        self.color_shift = 0

        # the text font we'll use most of the time
        self.font = pygame.font.SysFont("Arial", round(24 * self.scale), bold=True)

        # the list of py-game.surface instruments which we'll add to later
        self.instruments = []
        # these are the xy locations of all dynamic text in the instruments. The xy gets rescaled according to scale
        self.scale_xys = [(25, 22), (25, 57), (25, 92),
                          (205, 22), (205, 57), (205, 92),
                          (25, 133)]
        # xy location of the controls' status messages. They are separate as I couldn't figure out how to combine them
        # as the way I use scale_xys is very different)
        self.scale_controls = [(205, 133), (205, 158), (205, 183)]

    # updates the py-game.surface objects with up-to-date numbers
    def update_stats(self, lander, time, screen):
        # short-cut for the font
        f = self.font
        # make sure our controls is a list
        self.controls = []

        # color short-cuts
        gray = (200, 200, 200)
        yellow = (255, 255, 0)
        green = (0, 255, 0)

        # this is where we add 7 to color_shift and make sure it's within the range (0, 255) for rgb purposes
        # 7 gets added to it every tick, this is how we achieve the blinking 'emergency'-like effect
        self.color_shift += 7 % 255
        # flashing color red
        red = (128 + self.color_shift % 127, 0, 0)
        # flashing color orange
        orange = (255, 64 + self.color_shift % 127, 0)

        # the next few lines are very boring as they transform text into a py-game.surface object
        # we format some of the text to make it look more visually appealing when displayed
        self.fuel = f.render("FUEL: " + str(round(lander.fuel)), False, gray)
        # removing hours and milliseconds from the string
        self.time = f.render("TIME: " + str(datetime.now() - time)[2:-7], False, gray)
        self.damage = f.render("DAMAGE: " + str(lander.damage), False, gray)
        self.altitude = f.render("ALTITUDE: " + str(round(screen.get_height() - lander.y)), False, gray)
        self.x_velocity = f.render("X VELOCITY: " + str(round(abs(lander.x_velocity), 2)), False, gray)
        self.y_velocity = f.render("Y VELOCITY: " + str(round(abs(lander.y_velocity), 2)), False, gray)
        self.score = f.render("SCORE: " + str(lander.score), False, yellow)

        # iterates through the lander's controls
        for i in range(len(lander.controls)):
            # short-cut for control status
            control = lander.controls[i][0]
            # shortcut for time left for the control to be disabled
            time = lander.controls[i][1]

            # this is the part in text format (e.g "ENGINE -")
            txt = self.controls_messages[i]

            # if the control is 'permanently' destroyed
            if control == 2:
                # add destroyed to the text
                txt += "DESTROYED"
                # make it all red and flashy and add it to controls list
                self.controls.append(f.render(txt, False, red))

            # if the control is temporarily disabled
            elif control == 1:
                # add timer until it's fixed
                txt += "OFF FOR " + str(round(time, 1)) + "S"
                # flashy orange surface added to the controls list
                self.controls.append(f.render(txt, False, orange))

            # if the control is operational
            elif control == 0:
                # add ok status to it
                txt += "OK"
                # make it a surface with green colour and add it to the list
                self.controls.append(f.render(txt, False, green))

        # matches the order of coordinates in self.scale_xys
        self.instruments = [self.time, self.fuel, self.damage,
                            self.altitude, self.x_velocity, self.y_velocity,
                            self.score]

        # calls the display stats method
        self.display_stats(screen)

    # visualizes all stats
    def display_stats(self, screen):
        # short-cut for scale
        scale = self.scale

        # size of the default instrument window
        ib_x, ib_y = self.instruments_background.get_size()

        # re-scales the instruments window
        scaled_ib = pygame.transform.scale(self.instruments_background, (round(ib_x * scale), round(ib_y * scale)))

        # visualize the box
        screen.blit(scaled_ib, (5, 5))

        # iterates through all surfaces in instruments
        for i in range(len(self.instruments)):
            # index (i) of scale_xys and instruments are a "match"
            x, y = self.scale_xys[i]
            # changing location, depending on scale (0.00 to 1.00), visualizes the instrument on the game screen
            screen.blit(self.instruments[i], (x * scale, y * scale))

        # iterates through all surfaces in controls (these are the ones that blink)
        for i in range(len(self.controls)):
            # makes things more understandable, surface of control
            control_text = self.controls[i]
            # location of control
            x, y = self.scale_controls[i]
            # visualizes the control status on the game screen
            screen.blit(control_text, (x * scale, y * scale))


# Game class connects all 3 of our classes into a functioning game
class Game:
    # 1st line of the init dynamic attributes can be edited, this is done whenever a game class is called
    def __init__(self, x, y, fps, ui, n_pads, n_obstacles, n_meteors,
                 time=datetime.now(), lives=3, fuel=500, damage=0, score=0):
        # sets screen resolution based on input
        self.screen = pygame.display.set_mode((x, y))

        # sets raw background image
        self.bg_image = load_image("Resources/mars_background.png")
        # re-sizes bg_image to fit current game resolution
        self.background = pygame.transform.scale(self.bg_image, (x, y))

        # starts clock
        self.clock = pygame.time.Clock()
        self.tick_rate = fps

        # starts time
        self.start_time = time

        # starts py game window
        pygame.init()

        # creates the environment in the game
        self.n_pads = n_pads
        self.n_obstacles = n_obstacles
        self.n_meteors = n_meteors
        self.environment = Environment(screen=self.screen,
                                       pads_amount=self.n_pads,
                                       obstacle_amount=self.n_obstacles,
                                       meteor_amount=self.n_meteors)

        # creates a ship in the game
        self.lander = Lander(lives=lives,
                             fuel=fuel,
                             damage=damage,
                             screen=self.screen,
                             score=score)

        # creates stats
        self.ui_scale = ui
        self.stats = Stats(scale=self.ui_scale)

        # sets up the game window's caption
        pygame.display.set_caption("Mars Lander - " + str(self.lander.lives) + " lives left")

    # Creates a message on the whole screen
    def notification(self, txt, small):
        # short-cuts for colors
        black_t = (0, 0, 0, 128)
        white = (255, 255, 255)

        # get width and height of the game screen
        _, _, w, h = self.screen.get_rect()

        # creates a "box" the size of the game screen
        box = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        # fills it up with a 50% transparent black color
        box.fill(black_t)
        # visualizes the box
        self.screen.blit(box, (0, 0))

        # message is a py-game.surface version of the txt given when the function is called
        msg = pygame.font.SysFont("Arial", 50).render(txt, True, white)
        # shows it at the middle of the screen
        self.screen.blit(msg, (w/2-msg.get_width()/2, h/2-54))

        # different scenarios to display smaller text under the main message scenarios
        if txt == "PAUSED":
            txt = "PRESS P TO START"
            msg = pygame.font.SysFont("Arial", 25).render(txt, True, white)
            self.screen.blit(msg, (w / 2 - msg.get_width() / 2, h / 2))

        if small == 1:
            txt = "PRESS ANY KEY TO CONTINUE"
            msg = pygame.font.SysFont("Arial", 25).render(format(txt), True, white)
            self.screen.blit(msg, (w/2-msg.get_width()/2, h/2))

        # updates the game so that the notification can be seen
        pygame.display.update()

    # Pauses the game
    def pause(self, message, any_key=0, small=0):
        # calls for a notification
        self.notification(message, small)

        # the actual pause
        while True:
            # shortcut for event
            e = pygame.event.wait()
            # if we X the game screen
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if we press a key
            if e.type == pygame.KEYDOWN:
                # if we press P -> break, or if we just press a key and any_key is 1, also break
                if e.key == pygame.K_p or any_key == 1:
                    # break = un-pause the game
                    break

    # Re-runs the whole program with the cached variables
    def restart(self, lander):
        # I'm actually kind of surprised this worked out
        g = Game(x=self.screen.get_width(),
                 y=self.screen.get_height(),
                 fps=self.tick_rate,
                 ui=self.ui_scale,
                 n_pads=self.n_pads,
                 n_obstacles=self.n_obstacles,
                 n_meteors=self.n_meteors,
                 time=self.start_time,
                 lives=lander.lives,
                 fuel=lander.fuel,
                 damage=lander.damage,
                 score=lander.score)
        g.run()

    def run(self):
        # shortcuts
        start_time = self.start_time
        environment = self.environment
        lander = self.lander
        stats = self.stats
        screen = self.screen
        pads = environment.pad.pads
        obstacle = environment.obstacle
        meteor = environment.meteor

        # if the lander pilot has no more lives
        if lander.lives <= 0:
            # show a game over message and quit the game on any key press
            self.pause("GAME OVER | POINTS: " + str(lander.score), any_key=1, small=1)
            pygame.quit()
            quit()
        # game loop
        while True:
            # visualize the background on the game screen
            screen.blit(self.background, (0, 0))
            # update the stats
            stats.update_stats(time=start_time,
                               lander=lander,
                               screen=self.screen)
            # update the lander
            lander.update_lander(self.screen, self.tick_rate)
            # update the environment
            environment.update_environment()

            # for every event (key presses, mouse movements, window functions etc.)
            for event in pygame.event.get():
                # checks if we quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # if we press a key
                elif event.type == pygame.KEYDOWN:
                    # if that key is p
                    if event.key == pygame.K_p:
                        # pause the game
                        self.pause("PAUSED")

            # this allows for the holding down of keys, instead of just pressing them
            key = pygame.key.get_pressed()
            # different hold down key calls
            if key[pygame.K_SPACE]:
                # space = thrust
                lander.thrust(screen)
            if key[pygame.K_LEFT]:
                # left arrow - left rotation
                lander.rotate(-1)
            if key[pygame.K_RIGHT]:
                # right arrow - right rotation
                lander.rotate(1)

            # checks if lander has landed
            lander.is_landed(pads)
            # checks if lander is damaged
            lander.is_damaged(obstacle, meteor)

            # random chance, based on tick rate
            # this is 6% chance a second
            if randint(1, 500) == 1:
                # calls the creation of a meteor shower
                meteor.create_meteors()

            # this is 12% chance a second
            if randint(1, 250) == 1:
                # calls the random failure of a lander part
                lander.control_failure()

            # sets clock tick rate speed
            self.clock.tick(self.tick_rate)
            # calls for a visual update of everything
            pygame.display.update()


# Shortcut, avoids warnings from PyCharm
def load_image(image):
    # Mainly made this shortcut due to the .load method giving me a warning
    return pygame.image.load(image).convert_alpha()
    # this warning seems to occur to all pycharm users that use py-game


# Shortcut, used only at the beginning to make the game 'settings' look prettier
def r(s, f):
    # equals to a random number in the range s to f
    return randint(s, f)


# Sets up the game with the desired specifics and runs the game, crash velocity is >=2.5
game = Game(
            # game resolution
            x=1600, y=900,
            # game tick rate, all of the physics depend on it as of now
            fps=30,
            # ui scale, entered in percents (currently 80% of original size, can go above 100)
            ui=80,
            # number of pads
            n_pads=r(2, 5),
            # number of obstacles
            n_obstacles=r(5, 10),
            # number of meteors, 10-20 meteors works best in my experience, 5-10 are requirements
            n_meteors=r(5, 10)
            )
game.run()