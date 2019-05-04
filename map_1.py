"""Generates the Map for the Game"""
from scene import Scene
import config

SCENE = Scene(config.WIDTH, config.HEIGHT)
SCENE.castle_printer()
SCENE.x_selector()
SCENE.ground_maker(config.GROUND_LEVEL)

SCENE.obj_maker()

SCENE.cloud_maker_small()
SCENE.cloud_maker_big()

SCENE.walls.sort(key=SCENE.wall_sorter)
SCENE.pipes.sort(key=SCENE.pipe_sorter)
