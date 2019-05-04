"""Generates the main Engine of the Game"""
import os
import time
import config
from non_blocking_input import KBHit
from map_1 import SCENE
from characters import Mario, PowerUp
from objects import Bullet

KB = KBHit()
WIN = False

INSTANT = time.time()
MARIO = Mario(config.INITIAL_X, config.GROUND_LEVEL-2)
POWER = PowerUp(config.POWER_X+1, config.BRICK_HEIGHT_1-3)
POWER_DIS = 0

if MARIO.get_time() <= 200:
    os.system('aplay -q ./sounds/hurry_up.wav &')
i = 0
CH = "Point Saved"
os.system('aplay -q ./sounds/enter_level.wav &')

CURRENT = time.time()
os.system('aplay -q ./sounds/theme.wav &')

while not WIN and MARIO.get_lives() > 0:

    if time.time() - CURRENT > 88:
        os.system('aplay -q ./sounds/theme.wav &')
        CURRENT = time.time()

    if i % config.CHECKPOINT == 0:
        TO_DIS = CH
        MARIO.checkpoint = i
    else:
        TO_DIS = str(config.CHECKPOINT-i % config.CHECKPOINT)

    os.system('sleep 0.05')
    MARIO.dec_time()
    if KB.kbhit():
        KEY = KB.getch()
    else:
        KEY = " "
    if KEY == 'q':
        quit()

    if KEY == 'd':
        if time.time()-INSTANT > 0.1:
            MARIO.forward()
            INSTANT = time.time()

    if KEY == 'a':
        if time.time()-INSTANT > 0.1:
            MARIO.backward()
            INSTANT = time.time()

    if KEY == 'm' and MARIO.get_level() > 1:
        os.system('aplay -q ./sounds/fireball.wav &')
        SCENE.bullets.append(Bullet(MARIO.get_x()+i+2, MARIO.get_y()+1, 1))

    if KEY == 'n' and MARIO.get_level() > 1:
        os.system('aplay -q ./sounds/fireball.wav &')
        SCENE.bullets.append(Bullet(MARIO.get_x()+i-2, MARIO.get_y()+1, -1))

    if KEY == 'w':
        MARIO.start_jump()
        while MARIO.on_ground is not True:
            os.system('sleep 0.05')
            MARIO.jump_upd()
            if KB.kbhit():
                KEY = KB.getch()
            else:
                KEY = " "

            if KEY == 'd':
                if time.time()-INSTANT > 0.1:
                    MARIO.jump_forward()
                    INSTANT = time.time()

            if KEY == 'a':
                if time.time()-INSTANT > 0.1:
                    MARIO.jump_backward()
                    INSTANT = time.time()

            if KEY == 'm' and MARIO.get_level() > 1:
                os.system('aplay -q ./sounds/fireball.wav &')
                SCENE.bullets.append(
                    Bullet(MARIO.get_x()+i+2, MARIO.get_y()+1, 1))

            if KEY == 'n' and MARIO.get_level() > 1:
                os.system('aplay -q ./sounds/fireball.wav &')
                SCENE.bullets.append(
                    Bullet(MARIO.get_x()+i-2, MARIO.get_y()+1, -1))

            MARIO.detect_boundary()

            i = MARIO.mario_move(i, KEY)

            COLLIDED, Y_BOX, OFFSET, CH = MARIO.detect_collision(
                SCENE.temp[0:config.HEIGHT, MARIO.get_x()-1:MARIO.get_x()+2])
            MARIO.detect_floor(
                SCENE.temp[0:config.HEIGHT, MARIO.get_x()-1:MARIO.get_x()+2])

            SCENE.arrange_box(i, i+int(config.WIDTH/8))
            SCENE.obj_printer(i, i+int(config.WIDTH/8))

            if MARIO.pit_fall(SCENE.temp[MARIO.get_y()+3, MARIO.get_x()-1:MARIO.get_x()+2]):
                MARIO.reset()
                i = MARIO.checkpoint

            MARIO.detect_collision_x(SCENE.temp)

            if COLLIDED:
                if POWER_DIS == 0:
                    POWER_DIS = SCENE.destroy(MARIO.get_x()+OFFSET+i, Y_BOX, i)
                TEMP = SCENE.destroy(MARIO.get_x()+OFFSET+i, Y_BOX, i)
                if TEMP == -1 and POWER_DIS != 1:
                    POWER.visible = True
                    os.system('aplay -q ./sounds/mushroom_appears.wav &')
                elif TEMP != -1:
                    MARIO.inc_score(TEMP)

            if POWER_DIS == -1:
                SCENE.print_power(i, i+int(config.WIDTH/8), POWER)

            if POWER.taken(MARIO):
                POWER_DIS = 1

            WIN, BONUS = MARIO.detect_flag(SCENE.flag[0], i)
            if WIN:
                MARIO.inc_score(BONUS)
                break

            MARIO.inc_score(config.FREE_SCORE)
            MARIO.print(SCENE.temp)
            SCENE.bullet_printer(i, i+int(config.WIDTH/8))

            for enemy in SCENE.enemies:
                if (enemy.visible is True and MARIO.kill_enemy(enemy, i)):
                    os.system('aplay -q ./sounds/stomp.wav &')
                    MARIO.inc_score(config.SCORE_ENEMY)
                    break

                if(enemy.visible is True and enemy.kill_mario(MARIO, i)):
                    if MARIO.get_level() == 1:
                        MARIO.reset()
                        i = MARIO.checkpoint
                    elif MARIO.get_level() >= 2:
                        MARIO.level_dec()

            SCENE.enemy_printer(i, i+int(config.WIDTH/8), MARIO)

            os.system('clear')
            SCENE.print_box(MARIO.get_level())
            print("LIVES:"+str(MARIO.get_lives())+"\t\t\t\tDist. to CheckPoint:" +
                  str(TO_DIS) + "\t\t\t\t"+"SCORE:"+str(MARIO.get_score()) +
                  "\t\t\t\t"+"TIME:"+str(MARIO.get_time()))

    MARIO.detect_fall(SCENE.temp[MARIO.get_y()+3,
                                 MARIO.get_x()-1:MARIO.get_x()+2])
    MARIO.fall(SCENE.temp[0:config.HEIGHT, MARIO.get_x()-1:MARIO.get_x()+2])

    SCENE.arrange_box(i, i+int(config.WIDTH/8))
    SCENE.obj_printer(i, i+int(config.WIDTH/8))

    if MARIO.pit_fall(SCENE.temp[MARIO.get_y()+3, MARIO.get_x()-1:MARIO.get_x()+2]):
        MARIO.reset()
        i = MARIO.checkpoint

    for enemy in SCENE.enemies:
        if (enemy.visible is True and MARIO.kill_enemy(enemy, i)):
            os.system('aplay -q ./sounds/stomp.wav &')
            MARIO.inc_score(config.SCORE_ENEMY)
            break

        if(enemy.visible is True and enemy.kill_mario(MARIO, i)):
            if MARIO.get_level() == 1:
                MARIO.reset()
                i = MARIO.checkpoint
            elif MARIO.get_level() >= 2:
                MARIO.level_dec()

    WIN, BONUS = MARIO.detect_flag(SCENE.flag[0], i)
    MARIO.inc_score(BONUS)

    if POWER_DIS == -1:
        SCENE.print_power(i, i+int(config.WIDTH/8), POWER)
    POWER.taken(MARIO)

    SCENE.enemy_printer(i, i+int(config.WIDTH/8), MARIO)

    MARIO.detect_collision_x(SCENE.temp)
    MARIO.detect_boundary()

    if KEY != 'w':
        os.system('clear')

    MARIO.inc_score(config.FREE_SCORE)
    MARIO.print(SCENE.temp)
    SCENE.bullet_printer(i, i+int(config.WIDTH/8))
    SCENE.print_box(MARIO.get_level())

    print("LIVES:"+str(MARIO.get_lives())+"\t\t\t\tDist. to CheckPoint:" + str(TO_DIS) +
          "\t\t\t\t"+"SCORE:"+str(MARIO.get_score())+"\t\t\t\t"+"TIME:"+str(MARIO.get_time()))

    if MARIO.get_time() <= 0:
        MARIO.reset()

    if MARIO.get_lives() <= 0:
        SCENE.game_over(MARIO.get_score())

    i = MARIO.mario_move(i, KEY)

if WIN:
    MARIO.inc_score(MARIO.get_time()*100)
    for j in range(0, config.GROUND_LEVEL-config.FLAG_Y-5):
        os.system('clear')
        SCENE.arrange_box(i, i+int(config.WIDTH/8))
        SCENE.win_obj_printer(i, i+int(config.WIDTH/8))
        if MARIO.get_y() + 3 < config.GROUND_LEVEL:
            MARIO.inc_y()
        SCENE.flag[0].print_on_frame(SCENE.flag[0].get_x()-i, SCENE.temp, j)
        MARIO.print(SCENE.temp)
        SCENE.print_box(MARIO.get_level())
        print("LIVES:"+str(MARIO.get_lives())+"\t\t\t\tDist. to CheckPoint:" + str(TO_DIS) +
              "\t\t\t\t"+"SCORE:"+str(MARIO.get_score())+"\t\t\t\t"+"TIME:"+str(MARIO.get_time()))
        os.system('sleep 0.1')
    for j in range(config.FLAG_X, config.CASTLE_X-(2)*config.BLOCK_WIDTH):
        os.system('clear')
        SCENE.arrange_box(i, i+int(config.WIDTH/8))
        SCENE.win_obj_printer(i, i+int(config.WIDTH/8))
        SCENE.flag[0].print_on_frame(SCENE.flag[0].get_x(
        )-i, SCENE.temp, config.GROUND_LEVEL-config.FLAG_Y-5)
        MARIO.forward()
        MARIO.print(SCENE.temp)
        SCENE.print_box(MARIO.get_level())
        print("LIVES:"+str(MARIO.get_lives())+"\t\t\t\tDist. to CheckPoint:" + str(TO_DIS) +
              "\t\t\t\t"+"SCORE:"+str(MARIO.get_score())+"\t\t\t\t"+"TIME:"+str(MARIO.get_time()))

        os.system('sleep 0.1')

    SCENE.win(MARIO.get_score())
