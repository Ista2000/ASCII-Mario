"""Background Scene of the Game is Generated"""
import os
import random
import numpy as np
import config
from objects import Flag, Pipe, Unknown, Wall
from characters import Enemy


class Scene:
    """ Generates Scene for the Game """

    def __init__(self, width, height):
        self.width = config.WIDTH
        self.height = config.HEIGHT
        self.matrix = np.array([['0' for i in range(0, width)]
                                for j in range(0, height)])
        for i in range(0, width):
            self.matrix[0][i] = config.WALL
            self.matrix[height-1][i] = config.WALL
        self.temp = np.array([['0' for i in range(0, int(width/8))]
                              for j in range(0, height)])
        self.coords = []
        self.pipe_coords = []
        self.enemy_coords = []
        self.pipes = []
        self.walls = []
        self.unknowns = []
        self.enemies = []
        self.cloud_coords = []
        self.pit_coords = []
        self.cnt = 0
        self.flag = []
        self.bullets = []

    # Initialize the ground with the blocks
    def ground_maker(self, height):
        """Makes Ground for the Game"""
        for i in range(height, config.HEIGHT-1, 1):
            for j in range(0, config.WIDTH-1, 1):
                self.matrix[i, j] = config.BLOCK
        for pit in self.pit_coords:
            self.matrix[config.GROUND_LEVEL:config.GROUND_LEVEL +
                        4, pit[0]:pit[0]+pit[1]] = config.PIT

    # Initialize the clouds for the scene
    def cloud_maker_small(self):
        """Makes Small Clouds for the Game"""
        for _ in range(int(config.CLOUD_NUM/2)):
            i = self.cloud_coords.pop()
            self.matrix[i[1], i[0]:i[0]+4] = config.CLOUD
            self.matrix[i[1]+1, i[0]-1:i[0]+3] = config.CLOUD
            self.matrix[i[1]+2, i[0]-2:i[0]+2] = config.CLOUD

    def cloud_maker_big(self):
        """Makes Big Clouds for the Game"""
        for _ in range(int(config.CLOUD_NUM/2)):
            i = self.cloud_coords.pop()
            self.matrix[i[1], i[0]+1:i[0]+2] = config.CLOUD
            self.matrix[i[1]+1, i[0]:i[0]+3:2] = config.CLOUD
            self.matrix[i[1]+2, i[0]-1:i[0]+4] = config.CLOUD

    def x_selector(self):
        """Allots X-Coordinates to all Objects in the Game"""
        x_coord = config.X_ORD
        random.shuffle(x_coord)
        for i in range(config.BRICK_NUM):
            self.coords.append(
                [x_coord.pop(), config.BRICK_HEIGHT_1-config.JUMP, random.choice(config.TYPES)])

        x_coord = config.X_ORD
        random.shuffle(x_coord)
        self.coords.append(
            [config.POWER_X-5, config.BRICK_HEIGHT_1, "unknown"])
        self.coords.append([config.POWER_X, config.BRICK_HEIGHT_1, "unknown"])
        self.coords.append(
            [config.POWER_X+5, config.BRICK_HEIGHT_1, "unknown"])
        for i in range(config.UNKNOWN_NUM):
            self.coords.append(
                [x_coord.pop(), config.BRICK_HEIGHT_1, random.choice(config.TYPES)])

        x_coord = config.X_PIPE
        random.shuffle(x_coord)
        for i in range(config.ENEMY_NUM):
            self.pipe_coords.append(
                [x_coord.pop(), random.choice(config.Y_PIPE)])
            self.enemy_coords.append([self.pipe_coords[i][0]-2, config.GROUND_LEVEL -
                                      config.ENEMY_HEIGHT-1, random.choice(config.ENEMY_TYPES)])

        x_coord = config.X_CLOUD
        random.shuffle(x_coord)
        for i in range(config.CLOUD_NUM):
            self.cloud_coords.append(
                [x_coord.pop(), random.choice(config.Y_CLOUD)])

        x_coord = config.X_PIT
        random.shuffle(x_coord)
        for i in range(config.PIT_NUM):
            self.pit_coords.append(
                [x_coord.pop(), random.choice(config.PIT_WIDTH)])

    def castle_printer(self):
        """Makes the Castle for the Game"""
        i = 4
        for y_coord in range(config.GROUND_LEVEL-config.BLOCK_HEIGHT,
                             config.GROUND_LEVEL-4*config.BLOCK_HEIGHT-1, -config.BLOCK_HEIGHT):
            for x_coord in range(config.CASTLE_X+(4-i)*config.BLOCK_WIDTH,
                                 config.CASTLE_X+(3+i)*config.BLOCK_WIDTH, config.BLOCK_WIDTH):
                diff_block = config.GROUND_LEVEL-config.BLOCK_HEIGHT
                if y_coord == diff_block and x_coord == config.CASTLE_X+(3)*config.BLOCK_WIDTH:
                    continue
                self.coords.append([x_coord, y_coord, "brick"])
            i -= 1
        self.matrix[config.GROUND_LEVEL-6*config.BLOCK_HEIGHT:config.GROUND_LEVEL-4 *
                    config.BLOCK_HEIGHT, config.CASTLE_X+(3)*config.BLOCK_WIDTH+3] = config.FLAG
        self.matrix[config.GROUND_LEVEL-6*config.BLOCK_HEIGHT:config.GROUND_LEVEL-5*config.BLOCK_HEIGHT,
                    config.CASTLE_X+(3)*config.BLOCK_WIDTH+4:config.CASTLE_X+(3)*config.BLOCK_WIDTH+10] = config.CLOTH

    def obj_maker(self):
        """Makes all the Objects in the Game"""
        for i in self.coords:
            if i[2] == "brick":
                self.walls.append(Wall(i[0], i[1]))
            elif i[2] == "unknown":
                self.unknowns.append(Unknown(i[0], i[1]))

        for i in self.pipe_coords:
            self.pipes.append(Pipe(i[0], i[1]))

        for i in self.enemy_coords:
            self.enemies.append(Enemy(i[0], i[1], i[2]))

        self.flag.append(Flag(config.FLAG_X, config.FLAG_Y))

    def obj_printer(self, left, right):
        """Prints all the Objects in the Game"""
        for i in self.walls:
            x_coord = i.get_x()
            if i.visible and left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

        for i in self.unknowns:
            x_coord = i.get_x()
            if i.visible and left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

        for i in self.pipes:
            x_coord = i.get_x()
            if left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

        for i in self.flag:
            x_coord = i.get_x()
            if left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

    def win_obj_printer(self, left, right):
        """Makes Boundaries in the Game"""
        for i in self.walls:
            x_coord = i.get_x()
            if i.visible and left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

        for i in self.unknowns:
            x_coord = i.get_x()
            if i.visible and left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

        for i in self.pipes:
            x_coord = i.get_x()
            if left <= x_coord < right:
                i.print_on_frame(x_coord-left, self.temp)

    def enemy_printer(self, left, right, mario):
        """Prints all the Enemies in the Game"""
        for enemy in self.enemies:
            x_coord = enemy.get_x()
            y_coord = enemy.get_y()
            if left <= x_coord < right:
                if enemy.get_intel() == "smart":
                    if x_coord-left-1 > mario.get_x():
                        enemy.change_dir(-1)
                    elif x_coord-left-1 < mario.get_x():
                        enemy.change_dir(1)

                if enemy.pit_fall(self.temp[y_coord+3, x_coord-left:x_coord+3-left]):
                    enemy.destroy()
                if enemy.visible is True:
                    enemy.detect_collision_x(self.temp, left)
                    enemy.move()
                    enemy.print(x_coord-left-1, self.temp)
                else:
                    enemy.print_dead(x_coord-left-1, self.temp)

    def print_power(self, left, right, power):
        """Prints all the PowerUps in the Game"""
        x_coord = power.get_x()
        if left <= x_coord < right and power.visible is True:
            power.print(self.temp)

    def bullet_printer(self, left, right):
        """Prints all the Bullets fired by Mario"""
        for bullet in self.bullets:
            x_coord = bullet.get_x()
            y_coord = bullet.get_y()

            if left <= x_coord < right:
                if bullet.visible is True and bullet.get_direction() == 1:
                    bullet.forward()
                    try:
                        collision, who = bullet.detect_collision(
                            self.temp[y_coord, x_coord+1-left])
                        if collision:
                            bullet.destroyer()
                            if who == "enemy":
                                for enemy in self.enemies:
                                    for k in range(-3, 3, 1):
                                        if enemy.get_x() == x_coord+k:
                                            enemy.destroy()
                    except BaseException:
                        pass

                    bullet.print_on_frame(x_coord-left, self.temp)

                if bullet.visible is True and bullet.get_direction() == -1:
                    bullet.backward()
                    try:
                        collision, who = bullet.detect_collision(
                            self.temp[y_coord, x_coord-1-left])
                        if collision:
                            bullet.destroyer()
                            if who == "enemy":
                                for enemy in self.enemies:
                                    for k in range(-3, 3, 1):
                                        if enemy.get_x() == x_coord+k:
                                            enemy.destroy()
                    except BaseException:
                        pass
                    bullet.print_on_frame(x_coord-left, self.temp)

    def wall_sorter(self, elem):
        """Sorts Wall according to X-Coordinate"""
        return elem.get_x()

    def pipe_sorter(self, elem):
        """Sorts Pipes according to X-Coordinate"""
        return elem.get_x()

    def print_coin(self, x_coord, y_coord, offset):
        """Prints all the Coins in the Game"""
        self.temp[y_coord-1:y_coord+config.BLOCK_HEIGHT-1, x_coord-offset:x_coord +
                  config.BLOCK_WIDTH-offset] = config.UNKNOWN
        self.temp[y_coord+config.BLOCK_HEIGHT-1, x_coord -
                  offset:x_coord+config.BLOCK_WIDTH-offset] = " "
        self.temp[y_coord-4:y_coord-2, x_coord+1-offset] = config.L_COIN
        self.temp[y_coord-4:y_coord-2, x_coord+2-offset] = config.M_COIN
        self.temp[y_coord-4:y_coord-2, x_coord+3-offset] = config.R_COIN

    def print_broken_wall(self, x_coord, y_coord, offset):
        """Prints the Wall Animation in the Game"""
        self.temp[y_coord-1:y_coord+config.BLOCK_HEIGHT-1, x_coord-offset:x_coord +
                  config.BLOCK_WIDTH-offset] = config.BRICK
        self.temp[y_coord+config.BLOCK_HEIGHT-1, x_coord -
                  offset:x_coord+config.BLOCK_WIDTH-offset] = " "

    def destroy(self, x_coord, y_coord, offset):
        """Destroys all the Objects in the Game"""
        x_coord = x_coord - x_coord % config.BLOCK_WIDTH

        for i in self.walls:
            if i.get_x() == x_coord and i.get_y() == y_coord-2:
                os.system('aplay -q ./sounds/brick_block.wav &')
                i.destroyer()
                self.print_broken_wall(x_coord, y_coord-2, offset)
                return config.SCORE_BRICK

        for i in self.unknowns:
            if x_coord == config.POWER_X and i.get_x() == x_coord and i.get_y() == y_coord-2:
                return -1

            if i.get_x() == x_coord and i.get_y() == y_coord-2:
                os.system('aplay -q ./sounds/coin.wav &')
                i.destroyer()
                self.print_coin(x_coord, y_coord-2, offset)
                return config.SCORE_UNKNOWN
        return 0

    def arrange_box(self, left, right):
        """Arranges the Temporary Frame in the Game with respect to Mario"""
        y_coord = 0
        for i in range(self.height):
            x_coord = 0
            for j in range(left, right):
                try:
                    if(self.matrix[i, j+1] != '0'):
                        self.temp[y_coord, x_coord] = self.matrix[i, j+1]
                    else:
                        self.temp[y_coord, x_coord] = " "
                except BaseException:
                    continue
                x_coord = x_coord+1
            y_coord = y_coord+1

    def check_color(self, char, level):
        """Gives Colour to each Object in the Game"""
        var1 = char in (config.FACE, config.LEFT_HAND, config.RIGHT_HAND)
        var2 = char in (config.LEFT_LEG, config.RIGHT_LEG)
        if (var1 or var2):
            if level == 1:
                return config.CYAN
            if level == 2:
                return config.RED

        if char == config.BRICK:
            return config.YELLOW
        if char == config.ENEMY_LEFT_HEAD:
            return config.RED
        if char == config.ENEMY_RIGHT_HEAD:
            return config.RED
        if char == config.UNKNOWN:
            return config.BLUE
        if char == config.WALL:
            return config.WHITE
        if char == config.CLOUD:
            return config.WHITE
        if char == config.BLOCK:
            return config.MAGENTA
        if char == config.PIPE:
            return config.GREEN
        if char == config.BULLET:
            return config.RED
        if char in (config.L_TOMBSTONE, config.R_TOMBSTONE):
            return config.GRAY
        if char in (config.L_COIN, config.R_COIN, config.M_COIN):
            return config.YELLOW
        if char == config.PIT:
            return config.RED
        if char == config.FLAG:
            return config.MAGENTA
        return ""

    def print_box(self, level):
        """Prints the Temporary Frame"""
        for i in range(self.height):
            print(config.WHITE + config.WALL + config.BLANK, end="")
            for j in range(int(self.width/8)):
                print(self.check_color(
                    self.temp[i, j], level) + self.temp[i, j] + config.BLANK, end="")
            print(config.WHITE + config.WALL + config.BLANK)

    def game_over(self, score):
        """Prints Game Over as the Game Ends"""
        os.system('aplay -q ./sounds/game_over.wav &')
        image_game_over = [r"  ___   _   __  __ ___    _____   _____ ___ ",
                           r" / __| /_\ |  \/  | __|  / _ \ \ / / __| _ \\",
                           r"| (_ |/ _ \| |\/| | _|  | (_) \ V /| _||   /",
                           r" \___/_/ \_\_|  |_|___|  \___/ \_/ |___|_|_\\"]
        # os.system('clear')
        for i in image_game_over:
            print("\t\t\t\t\t\t" + i)
        print()
        print("\t\t\t\t\t\t\t\tFINAL SCORE :" + str(score))
        os.system('pkill -kill aplay')
        quit()

    def win(self, score):
        """Displays the Win Message in the Game"""
        print("\t\t\t\t\t\t\t\tYOU WIN")
        print("\t\t\t\t\t\t\t   FINAL SCORE :" + str(score))
        os.system('pkill -kill aplay')
        quit()
