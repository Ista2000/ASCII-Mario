"""Initializes the Characters for the game"""
import os
import config


class Character():
    """Initializes all the Characters of the Game"""

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.visible = True
        self.on_ground = True

    def forward(self):
        """Move Forward"""
        self._x += config.VELOCITYX

    def backward(self):
        """Move Backward"""
        self._x -= config.VELOCITYX

    def get_x(self):
        """Get_x"""
        return self._x

    def get_y(self):
        """Get_y"""
        return self._y

    def destroy(self):
        """Destroys the Object"""
        self.visible = False

    def pit_fall(self, cells):
        """Controls death in pits"""
        try:
            if cells[0] == config.PIT or cells[1] == config.PIT or cells[2] == config.PIT:
                return True
        except BaseException:
            pass
        return False


class Mario(Character):
    """Initializes Mario in the Game"""

    def __init__(self, x, y, ch=config.EMPTY):
        super().__init__(x, y)
        self.type = ch
        self.level = 1
        self.velocity_y = 0
        self.velocity_x = config.VELOCITYX
        self._lives = 3
        self._score = 0
        self.checkpoint = config.INITIAL_X
        self.time = config.TIME

    def inc_score(self, inc):
        """Increments Score"""
        self._score += inc

    def get_score(self):
        """Gets Score"""
        return self._score

    def inc_y(self):
        """Increments y"""
        self._y += 1

    def get_lives(self):
        """Gets Life"""
        return self._lives

    def reset(self):
        """Reset Game after Death of Mario"""
        self._lives -= 1
        self._x = self.checkpoint
        self.time = config.TIME

    def get_time(self):
        """Returns Time"""
        return self.time

    def dec_time(self):
        """Time Counter"""
        self.time -= 1

    def level_inc(self):
        """Increments Level"""
        self.level += 1

    def level_dec(self):
        """Decrements Level"""
        os.system('aplay -q ./sounds/player_down.wav &')
        self.level -= 1

    def get_level(self):
        """Returns Level"""
        return self.level

    def print(self, scene):
        """Prints Mario"""
        scene[self._y, self._x] = config.FACE
        scene[self._y+1, self._x] = config.BACK
        scene[self._y+1, self._x-1] = config.LEFT_HAND
        scene[self._y+1, self._x+1] = config.RIGHT_HAND
        scene[self._y+2, self._x-1] = config.LEFT_LEG
        scene[self._y+2, self._x+1] = config.RIGHT_LEG

    def jump_forward(self):
        """Jumps Forward"""
        self._x += config.VELOCITYX_INC

    def jump_backward(self):
        """Jumps Backward"""
        self._x -= config.VELOCITYX_INC

    def start_jump(self):
        """Mario Jumps"""
        if self.on_ground is True:
            os.system('aplay -q ./sounds/jump.wav &')
            self.velocity_y = config.VELOCITYY
            self.on_ground = False

    def jump_upd(self):
        """Updates Coordinates according to Jump"""
        self.velocity_y += config.GRAVITY
        self._y += self.velocity_y

        if self._y >= config.GROUND_LEVEL:
            self._y = config.GROUND_LEVEL - 3
            self.velocity_y = 0
            self.on_ground = True

    def detect_fall(self, cells):
        """Detects Fall"""
        try:
            var1 = cells[0] == config.EMPTY and cells[1] == config.EMPTY
            var2 = cells[0] != config.CLOUD and cells[1] != config.CLOUD
            var3 = cells[2] == config.EMPTY and cells[2] != config.CLOUD
            var4 = cells[0] == config.BULLET or cells[1] == config.BULLET
            var5 = cells[2] == config.BULLET
            if var1 and var2 and var3:
                self.on_ground = False
                return True
            if var4 or var5:
                self.on_ground = False
                return True
        except BaseException:
            pass
        return False

    def detect_collision_x(self, matrix):
        """Detect Collision in X"""
        cloud_sym = config.CLOUD
        temp = self._x
        var1 = (matrix[self._y, self._x+2] !=
                " " and matrix[self._y, self._x+2] != cloud_sym)
        var2 = (matrix[self._y+1, self._x+2] !=
                " " and matrix[self._y+1, self._x+2] != cloud_sym)
        var3 = (matrix[self._y+2, self._x+2] !=
                " " and matrix[self._y+2, self._x+2] != cloud_sym)

        if var1 or var2 or var3:
            self._x = temp - 1
            return True, "right"

        var1 = (matrix[self._y, self._x-2] !=
                " " and matrix[self._y, self._x-2] != cloud_sym)
        var2 = (matrix[self._y+1, self._x-2] !=
                " " and matrix[self._y+1, self._x-2] != cloud_sym)
        var3 = (matrix[self._y+2, self._x-2] !=
                " " and matrix[self._y+2, self._x-2] != cloud_sym)

        if var1 or var2 or var3:
            self._x = temp + 1
            return True, "left"

        return False, None

    def detect_boundary(self):
        """Detect the Boundary"""
        if self._x < 1:
            self._x = 1

        if self._x > config.WIDTH-1:
            self._x = config.WIDTH - 1

        if self._y <= 0:
            self.velocity_y = 0
            self._y = 1

    def detect_collision(self, matrix):
        """Detect the Collision"""
        for i in range(self._y-1, self._y-self.velocity_y-config.GRAVITY-1):
            if (matrix[i-1, 1] != config.EMPTY and matrix[i-1, 1] != config.CLOUD):
                self._y = i
                self.velocity_y = 0
                return True, i-1, 0, matrix[i-1, 1]
            if (matrix[i-2, 0] != config.EMPTY and matrix[i-2, 0] != config.CLOUD):
                self._y = i
                self.velocity_y = 0
                return True, i-1, -1, matrix[i-2, 0]
            if (matrix[i-2, 2] != config.EMPTY and matrix[i-2, 2] != config.CLOUD):
                self._y = i
                self.velocity_y = 0
                return True, i-1, 1, matrix[i-2, 2]
        return False, -1, 2, 0

    def detect_floor(self, matrix):
        """Detect the Floor for Mario"""
        for i in range(self._y-1, self._y-self.velocity_y+config.GRAVITY-1, -1):
            var1 = matrix[i+4, 1] != config.EMPTY or matrix[i +
                                                            4, 0] != config.EMPTY
            if var1 or matrix[i+4, 2] != config.EMPTY:
                self._y = i-1
                self.velocity_y = 0
                self.on_ground = True
                break

        if(matrix[self._y+2, 1] != config.EMPTY):
            self._y -= 1

    def fall(self, matrix):
        """Mario's Fall"""
        if self.on_ground is False:
            self.jump_upd()
        try:
            self.detect_floor(matrix)
        except BaseException:
            pass

    def mario_move(self, i, key):
        """Controls Movement of Mario"""
        if (self._x > int(config.WIDTH/16) and self._x < int(15*config.WIDTH/16)):
            if key == 'd':
                i = i+config.VELOCITYX_INC
                self.jump_backward()

            if key == 'a':
                i = i-config.VELOCITYX_INC
                self.jump_forward()

        return i

    def kill_enemy(self, enemy, offset):
        """Detects the kill of Enemy"""
        # print(enemy._x-2-offset, self._x, enemy._x+3-offset ,self._y + 2 ,enemy._y)
        var1 = enemy.get_x()-2-offset <= self._x and self._x <= enemy.get_x()+3-offset
        var2 = self._y + 2 == enemy.get_y() or self._y + 3 == enemy.get_y()
        if (var1 and var2):
            enemy.destroy()
            return True
        return False

    def detect_flag(self, flag, offset):
        """Detect Level Completion"""
        for i in range(2, -1, -1):
            if self._x + i == flag.get_x() - offset:
                bonus = int((config.GROUND_LEVEL - self._y)*1000)
                os.system('aplay -q ./sounds/level_clear.wav &')
                return True, bonus
        return False, 0


class Enemy(Character):
    """Initializes Enemiees in the Game"""

    def __init__(self, x, y, intel):
        super().__init__(x, y)
        self.velocity_x = config.ENEMY_VELOCITY_X
        self.alive = True
        self.intel = intel

    def move(self):
        """Enemy Moves"""
        self._x += self.velocity_x

    def get_intel(self):
        """Enemy Intel"""
        return self.intel

    def print(self, x_coord, scene):
        """Prints Enemy"""
        scene[self._y, x_coord] = config.ENEMY_LEFT_HEAD
        scene[self._y, x_coord+1] = config.ENEMY_RIGHT_HEAD
        scene[self._y+1, x_coord] = config.ENEMY_LEFT_LEG
        scene[self._y+1, x_coord+1] = config.ENEMY_RIGHT_LEG

    def print_dead(self, x_coord, scene):
        """Prints Dead Enemy"""
        scene[self._y, x_coord] = config.L_TOMBSTONE
        scene[self._y, x_coord+1] = config.R_TOMBSTONE
        scene[self._y+1, x_coord] = '|'
        scene[self._y+1, x_coord+1] = '|'

    def change_dir(self, direction):
        """Enemy Changes Direction on Collision"""
        if direction == -1:
            self.velocity_x = -1 * abs(self.velocity_x)
        elif direction == 1:
            self.velocity_x = abs(self.velocity_x)

    def detect_collision_x(self, matrix, subtracter):
        """Enemy X Collision Detector"""
        try:
            var1 = matrix[self._y, self._x+1-subtracter] != " "
            var2 = matrix[self._y+1, self._x+1-subtracter] != " "
            var3 = matrix[self._y+2, self._x+1-subtracter] != " "
            var4 = matrix[self._y, self._x-2-subtracter] != " "
            var5 = matrix[self._y+1, self._x-2-subtracter] != " "
            var6 = matrix[self._y+2, self._x-2-subtracter] != " "

            if(var1 and var2 and var3):
                self.velocity_x = -1 * self.velocity_x

            elif(var4 and var5 and var6):
                self.velocity_x = -1 * self.velocity_x
        except BaseException:
            pass

    def kill_mario(self, mario, offset):
        """Detects Mario killed by Enemy"""
        if(self._x - offset - 1 == mario.get_x() + 2 and mario.get_y() == self._y - 1):
            return True

        if(self._x + 2 - offset == mario.get_x() and mario.get_y() == self._y - 1):
            return True

        return False


class PowerUp(Character):
    """Initializes PowerUps in the Game"""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.visible = False

    def print(self, scene):
        """Prints the PowerUp Symbol"""
        x_coord = self.get_x()
        y_coord = self.get_y()
        scene[y_coord, x_coord] = config.POWER
        scene[y_coord, x_coord+2] = config.POWER
        scene[y_coord+1, x_coord+1] = config.POWER
        scene[y_coord+2, x_coord] = config.POWER
        scene[y_coord+2, x_coord+2] = config.POWER

    def taken(self, mario):
        """Detect the TakingUp of Power by Mario"""
        var1 = mario.get_x()-3 <= self._x <= mario.get_x()+3
        var2 = mario.get_y() <= self._y <= mario.get_y()+3
        if var1 and var2 and self.visible:
            os.system('aplay -q ./sounds/power-up.wav &')
            self.destroy()
            if mario.get_level() == 1:
                mario.level_inc()
            return True

        return False
