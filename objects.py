"""Describes the Properties of all the Objects in the Game"""
import config


class Object():
    """Object Parent Class"""

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.visible = True

    def get_x(self):
        """Gets X-Coord"""
        return self._x

    def get_y(self):
        """Gets Y-Coord"""
        return self._y

    def destroyer(self):
        """Destroys Objects"""
        self.visible = False


class Wall(Object):
    """Defines the Wall Object in the Game"""

    def print_on_frame(self, x_coord, matrix):
        """Prints Wall on the Game Background"""
        matrix[self._y:self._y+config.BLOCK_HEIGHT,
               x_coord:x_coord+config.BLOCK_WIDTH] = config.BRICK


class Unknown(Object):
    """Defines the Brick with Coins Object in the Game"""

    def print_on_frame(self, x_coord, matrix):
        """Prints Brick with Coins on the Game Background"""
        matrix[self._y:self._y+config.BLOCK_HEIGHT,
               x_coord:x_coord+config.BLOCK_WIDTH] = config.UNKNOWN


class Pipe(Object):
    """Defines the Pipe Object in the Game"""

    def print_on_frame(self, x_coord, matrix):
        """Prints Pipes on the Game Background"""
        matrix[self._y, x_coord-1:x_coord+config.PIPE_WIDTH+1] = config.BRICK
        matrix[self._y+1:config.GROUND_LEVEL+1,
               x_coord:x_coord+config.PIPE_WIDTH] = config.PIPE


class Flag(Object):
    """Defines the Flag Object in the Game"""

    def print_on_frame(self, x_coord, matrix, down=0):
        """Prints Flag on the Game Background"""
        try:
            matrix[self._y:config.GROUND_LEVEL+1, x_coord] = config.FLAG
            for i in range(self._y+down, self._y+5+down):
                for j in range(10):
                    matrix[i, x_coord+j+1] = config.CLOTH
        except BaseException:
            pass


class Bullet(Object):
    """Defines the Bullet Object in the Game"""

    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.velocity_x = config.BULLET_VELX
        self.direction = direction

    def print_on_frame(self, x_coord, matrix):
        """Prints Bullet on the Game Background"""
        if self.direction == 1:
            matrix[self._y, x_coord] = config.BULLET
        elif self.direction == -1:
            matrix[self._y, x_coord] = config.BULLET

    def forward(self):
        """Bullet Moves Forward"""
        self._x += self.velocity_x

    def backward(self):
        """Bullet Moves Backward"""
        self._x -= self.velocity_x

    def get_direction(self):
        """Bullet Gets Direction"""
        return self.direction

    def detect_collision(self, cell):
        """Detect Collision of Bullet with other Objects in the Game"""
        var1 = cell in (config.EMPTY, config.CLOUD,
                        config.LEFT_HAND, config.RIGHT_HAND, config.BACK)
        var2 = cell is not config.PIPE
        if var1 and var2:
            return False, "empty"

        if (self.direction == 1 and cell == config.ENEMY_LEFT_HEAD):
            return True, "enemy"
        if (self.direction == -1 and cell == config.ENEMY_RIGHT_HEAD):
            return True, "enemy"

        return True, "block"

    def __del__(self):
        pass
