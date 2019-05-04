"""Declares all the Constant Variables to be used in the Game"""

#import os
#HEIGHT, WIDTH = os.popen('stty size', 'r').read().split()
try:
    LEVEL = int(input("Enter level number [[1],2,3] : ") or "1")
except BaseException:
    LEVEL = 1

HEIGHT, WIDTH = 41, 158
WIDTH = (int(WIDTH) - 4) * 8
HEIGHT = int(HEIGHT) - 2
SCREEN_WIDTH = int(WIDTH/8)

INITIAL_X = 15
GROUND_LEVEL = int(3*HEIGHT/4 + 4)
CLOUD_HEIGHT = int(HEIGHT/8)
BRICK_HEIGHT_1 = int(9*HEIGHT/16)
CHECKPOINT = 300
JUMP = GROUND_LEVEL - BRICK_HEIGHT_1
UNKNOWN = u'\U000025A0'
WALL = '*'
EMPTY = ' '
PIPE = '.'
PIT = '^'
BLOCK = '_'
BRICK = u'\U000025A1'
L_BOTTOM = u'\U00002514'
R_TOP = u'\U00002510'
L_TOP = u'\U0000250C'
R_BOTTOM = u'\U00002518'
CLOUD = u'\U000025B3'
CLOTH = u'\U000025B3'
BULLET = u'\U00002022'
L_COIN = '('
R_COIN = ')'
M_COIN = '.'
FLAG = '-'

CLOUD_NUM = 50
if LEVEL == 1:
    PIT_NUM = 10
    BRICK_NUM = 100
    UNKNOWN_NUM = 100
    ENEMY_NUM = 10
    PIT_WIDTH = [3, 5]
elif LEVEL == 2:
    PIT_NUM = 20
    BRICK_NUM = 75
    UNKNOWN_NUM = 75
    ENEMY_NUM = 20
    PIT_WIDTH = [5, 6]
elif LEVEL == 3:
    PIT_NUM = 30
    BRICK_NUM = 50
    UNKNOWN_NUM = 50
    ENEMY_NUM = 30
    PIT_WIDTH = [8, 10]


# MARIO
LEFT_HAND = '/'
RIGHT_HAND = '\\'
LEFT_LEG = '/'
RIGHT_LEG = '\\'
BACK = '|'
FACE = 'O'

CROWN = 'w'
GRAVITY = 1
VELOCITYY = int(-JUMP/2)
VELOCITYX = 2
VELOCITYX_INC = 2
ENEMY_VELOCITY_X = -1
BULLET_VELX = 1
BLOCK_HEIGHT = 3
BLOCK_WIDTH = 5
PIPE_WIDTH = 3
ENEMY_HEIGHT = 1
TIME = 2000
FREE_SCORE = 1

GRAY = "\033[1;30m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
BLANK = "\033[1;m"

L_TOMBSTONE = u'\U000025DC'
R_TOMBSTONE = u'\U000025DD'

SCORE_BRICK = 20
SCORE_UNKNOWN = 100
SCORE_ENEMY = 500
# ENEMY
ENEMY_FACE = "O"
ENEMY_LEFT_HEAD = "["
ENEMY_RIGHT_HEAD = "]"
ENEMY_LEFT_LEG = "'"
ENEMY_RIGHT_LEG = "'"

POWER_X = 15
POWER = '*'
X_ORD = []
for i in range(70, WIDTH-150, 5):
    X_ORD.append(i)

X_PIT = []
for i in range(100, WIDTH - 200, 15):
    X_PIT.append(i)


X_PIPE = []
for i in range(100, WIDTH - 150, 25):
    X_PIPE.append(i)

X_CLOUD = []
for i in range(20, WIDTH - 150, 10):
    X_CLOUD.append(i)
Y_CLOUD = [int(HEIGHT/10), int(HEIGHT/10-1), int(HEIGHT/10-2)]

PIPE_H = int((3*BRICK_HEIGHT_1 - JUMP)/2)
Y_PIPE = [PIPE_H+1, PIPE_H+2, PIPE_H]
FLAG_X = int(29*WIDTH/32)
FLAG_Y = int(3*HEIGHT/8)

CASTLE_X = int(15*WIDTH/16)

TYPES = ["brick", "unknown"]
ENEMY_TYPES = ["normal", "smart"]
