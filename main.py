# TODO:
# problemet er, at background surface 
#en funktion til at finde mængen af x og y tiles ud fra størrelsen af billede

from tkinter import CENTER
from turtle import position
import pygame, json, sys, math
from pygame.locals import *

from Classes.saving import *
from areas.areas import *

TILE_SIZE = 16
SCALE_FACTOR = 4
TILE_SCALE = TILE_SIZE * SCALE_FACTOR
WALKING_SPEED = 2
RATIO = 1.5

pygame.init()
mainClock = pygame.time.Clock()
pygame.display.set_caption("Hello World!")

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((15*TILE_SCALE, 10*TILE_SCALE), pygame.RESIZABLE)

current_screen_dimensions = pygame.display.get_surface().get_size()

background_surface = pygame.Surface((current_screen_dimensions[0]/SCALE_FACTOR, current_screen_dimensions[1]/SCALE_FACTOR))
dirt = pygame.image.load("assets/images/Dirt.png")
grass = pygame.image.load("assets/images/Grass.png")
player = pygame.image.load("assets/images/Player.png")

tiles = [dirt, grass, dirt, grass, dirt, grass]

def get_screen_center(dimensions):
    return ((dimensions[0]/2 - 0.5)*TILE_SIZE, (dimensions[1]/2 - 0.5)*TILE_SIZE)

def find_tiles_avaliable (dimensions):
    x = round(dimensions[0]/TILE_SCALE)
    y = round(dimensions[1]/TILE_SCALE)
    if x < y*1.5:
        y = round(x/1.5)
    else:
        x = round(y*1.5)
    return (x, y)

xy = find_tiles_avaliable(current_screen_dimensions)
screen_center = get_screen_center(xy)




fullscreen = False

position_offset = [0,0]

moving = False
moving_left, moving_right, moving_up, moving_down = False, False, False, False
left_momentum, right_momentum, up_momentum, down_momentum = False, False, False, False

latest_direction = ""
current_directions = []


current_area = plains

font = pygame.font.Font('freesansbold.ttf', 32)

run_queue = []

def run_1_tile(direction):
    x = 0
    while x < TILE_SIZE:
        run_queue.append(direction)
        x += 1

#game loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    current_screen_dimensions = [screen.get_width(), screen.get_height()]
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(current_screen_dimensions, pygame.RESIZABLE)
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                moving = True
                if event.key == K_a:
                    latest_direction = "left"
                if event.key == K_d:
                    latest_direction = "right"
                if event.key == K_w:
                    latest_direction = "up"
                if event.key == K_s:
                    latest_direction = "down"
                current_directions.append(latest_direction)
                
        
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                moving = False
                if event.key == K_a:
                    current_directions.pop(current_directions.index("left"))
                if event.key == K_d:
                    current_directions.pop(current_directions.index("right"))
                if event.key == K_w:
                    current_directions.pop(current_directions.index("up"))
                if event.key == K_s:
                    current_directions.pop(current_directions.index("down"))

        if event.type == VIDEORESIZE:
            if not fullscreen:
                new_size = find_tiles_avaliable((event.w, event.h))
                screen = pygame.display.set_mode((new_size[0]*TILE_SCALE, new_size[1]*TILE_SCALE), pygame.RESIZABLE)
                current_screen_dimensions = (new_size[0]*TILE_SCALE, new_size[1]*TILE_SCALE)
                xy = find_tiles_avaliable(current_screen_dimensions)
                screen_center = get_screen_center(xy)
                background_surface = pygame.Surface((current_screen_dimensions[0]/SCALE_FACTOR, current_screen_dimensions[1]/SCALE_FACTOR))

        
        if event.type == QUIT:
            with open(f"save_{1}.txt", "w") as save:
                json.dump(save_data[1].__dict__, save)
            pygame.quit()
            sys.exit()
    


    #animation
    if len(current_directions):
        direction = current_directions[-1]

        if not len(run_queue):
            run_1_tile(direction)
        elif direction not in run_queue:
            run_1_tile(direction)

    if len(run_queue):
        direction = run_queue[0]
        if direction == "left":
            position_offset[0] += WALKING_SPEED
        elif direction == "right":
            position_offset[0] -= WALKING_SPEED
        elif direction == "up":
            position_offset[1] += WALKING_SPEED
        elif direction == "down":
            position_offset[1] -= WALKING_SPEED
        run_queue = run_queue[WALKING_SPEED:]
        


    rounded_offset = [int(position_offset[0]), int(position_offset[1])]

    #rendering
    screen.fill((50,0,50))
    background_surface.fill((50,50,50))
    y = 0
    for row in current_area.collision_map:
            x = 0
            for tile in row:
                background_surface.blit(tiles[tile], (x*TILE_SIZE + rounded_offset[0] + (screen_center[0] - current_area.x*TILE_SIZE), y*TILE_SIZE + rounded_offset[1] + (screen_center[1] - current_area.y*TILE_SIZE)))
                x += 1
            y += 1
    background_surface.blit(player, screen_center)


    background_surface_scaled = pygame.transform.scale(background_surface, current_screen_dimensions)
    #difference
    
    screen.blit(background_surface_scaled, (0,0))
    text = font.render(f"{round(mainClock.get_fps())}, {current_directions}, {position_offset}, ", True, (0,0,100), (100,0,0))
    screen.blit(text, (0,0))

    pygame.display.update()
    mainClock.tick(60)