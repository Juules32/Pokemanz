# TODO:
#find en måde at læse player og currentplayer samtidig
# 0: walkable
# 1: walls
# 2: warps
# 3: default spawn
# 4: interactable walls
# 5: interactable ground
# 6: visible pickup
# 7: insivible pickup

#imports
from asyncio.windows_events import NULL
from ctypes import sizeof
from turtle import pos
import pygame, json, sys
from pygame.locals import *
from Classes.areas import *
from Classes.player import *

#constants
TILE_SIZE = 16
SCALE_FACTOR = 4
TILE_SCALE = TILE_SIZE * SCALE_FACTOR
WALKING_SPEED = 2
RATIO = 1.5

#initialisations
pygame.init()
pygame.display.set_caption("Hello World!")
mainClock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

#displays
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((15*TILE_SCALE, 10*TILE_SCALE), pygame.RESIZABLE)
current_screen_dims = pygame.display.get_surface().get_size()
sprite_surface = pygame.Surface((current_screen_dims[0]/SCALE_FACTOR, current_screen_dims[1]/SCALE_FACTOR))

trans = {
    (-1,0): "left",
    (1,0): "right",
    (0,-1): "up",
    (0,1): "down"
}

#image loading
people = {
    "sailor1": pygame.image.load("Assets/sailor1.png")
}

player_sprite = {
    "left_0": pygame.image.load("Assets/left_0.png"),
    "left_1": pygame.image.load("Assets/left_1.png"),
    "left_2": pygame.image.load("Assets/left_2.png"),
    "right_0": pygame.image.load("Assets/right_0.png"),
    "right_1": pygame.image.load("Assets/right_1.png"),
    "right_2": pygame.image.load("Assets/right_2.png"),
    "up_0": pygame.image.load("Assets/up_0.png"),
    "up_1": pygame.image.load("Assets/up_1.png"),
    "up_2": pygame.image.load("Assets/up_2.png"),
    "down_0": pygame.image.load("Assets/down_0.png"),
    "down_1": pygame.image.load("Assets/down_1.png"),
    "down_2": pygame.image.load("Assets/down_2.png")
}

def get_screen_center(dims):
    return ((dims[0]/2 - 0.5)*TILE_SIZE, (dims[1]/2 - 0.5)*TILE_SIZE)

def find_tiles_avaliable (dims):
    x = round(dims[0]/TILE_SCALE)
    y = round(dims[1]/TILE_SCALE)
    return (x, y)

def size_check (dims, min_display_size = [9 * TILE_SCALE, 6 * TILE_SCALE]):
    w = dims[0]
    h = dims[1]
    if dims[0] < min_display_size[0]:
        w = min_display_size[0]
    if dims[1] < min_display_size[1]:
        h = min_display_size[1]    
    return (w, h)

def run_1_tile(dir):
    x = 0
    while x < TILE_SIZE:
        run_queue.append(dir)
        x += 1
    current_player_data.pos[0] += dir[0]
    current_player_data.pos[1] += dir[1]

#game loop variable inits
xy = find_tiles_avaliable(current_screen_dims)
screen_center = get_screen_center(xy)
fullscreen = False
pos_offset = [0,0]
latest_dir = None
current_dirs = []
stored_size = [15, 10]
run_queue = []


#read save
with open(f"Save Data/save_{1}.txt") as save:
    data = json.load(save)
    for key, value in data.items():
        setattr(player, key, value)

save.close()
with open(f"Save Data/save_{1}.txt") as save:
    data = json.load(save)
    for key, value in data.items():
        setattr(current_player_data, key, value)
save.close()

current_area = plains

total_offset = 0
count = 0
stance = 0


#game loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    stored_size = current_screen_dims
                    xy = find_tiles_avaliable(monitor_size)
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(stored_size, pygame.RESIZABLE)
                current_screen_dims = (xy[0]*TILE_SCALE, xy[1]*TILE_SCALE)
                screen_center = get_screen_center(xy)
                sprite_surface = pygame.Surface((current_screen_dims[0]/SCALE_FACTOR, current_screen_dims[1]/SCALE_FACTOR))
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                if event.key == K_a:
                    latest_dir = (-1, 0)
                if event.key == K_d:
                    latest_dir = (1, 0)
                if event.key == K_w:
                    latest_dir = (0, -1)
                if event.key == K_s:
                    latest_dir = (0, 1)
                current_dirs.append(latest_dir)
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                if event.key == K_a:
                    current_dirs.pop(current_dirs.index((-1, 0)))
                if event.key == K_d:
                    current_dirs.pop(current_dirs.index((1, 0)))
                if event.key == K_w:
                    current_dirs.pop(current_dirs.index((0, -1)))
                if event.key == K_s:
                    current_dirs.pop(current_dirs.index((0, 1)))
        if event.type == VIDEORESIZE:
            if not fullscreen:
                current_screen_dims = (event.w, event.h)
                current_screen_dims = size_check(current_screen_dims)
                stored_size = current_screen_dims
                xy = find_tiles_avaliable(current_screen_dims)
                screen = pygame.display.set_mode(current_screen_dims, pygame.RESIZABLE)
                screen_center = get_screen_center(xy)
                sprite_surface = pygame.Surface((current_screen_dims[0]/SCALE_FACTOR, current_screen_dims[1]/SCALE_FACTOR))
        if event.type == QUIT:
            with open(f"Save Data/save_{1}.txt", "w") as save:
                json.dump(current_player_data.__dict__, save)
            pygame.quit()
            sys.exit()


    #checking if player can move
    if len(current_dirs):
        dir = current_dirs[-1]
        wants_to_go = [current_player_data.pos[0] + dir[0], current_player_data.pos[1] + dir[1]]
        if wants_to_go[0] < current_area.w and wants_to_go[0] >= 0 and wants_to_go[1] < current_area.h and wants_to_go[1] >= 0:
            if current_area.collision_map[wants_to_go[1]][wants_to_go[0]] == 0:
                if not len(run_queue):
                    run_1_tile(dir)
                # never two steps from 1 input and never more than two in queue
                elif dir not in run_queue and len(run_queue) <= 16:
                    run_1_tile(dir)
            else:
                current_player_data.facing = trans[dir]
        else:
            current_player_data.facing = trans[dir]


    

    #animation
    if len(run_queue):
        dir = run_queue[0]
        current_player_data.facing = trans[dir]
        pos_offset[0] += dir[0] * WALKING_SPEED
        pos_offset[1] += dir[1] * WALKING_SPEED
        length = len(run_queue)
        if length % TILE_SIZE == 0:
            count += 1
            stance = count % 2 + 1
        elif length % TILE_SIZE == 8:
            stance = 0



        run_queue = run_queue[WALKING_SPEED:]

    else:
        
        count = 0
        stance = 0

    total_offset = (-pos_offset[0] + screen_center[0] - player.pos[0]*TILE_SIZE, -pos_offset[1] + screen_center[1] - player.pos[1]*TILE_SIZE)

    #rendering
    sprite_surface.fill((20,20,20))
    sprite_surface.blit(current_area.background_sprite, total_offset)
    sprite_surface.blit(current_area.foreground_sprite, total_offset)
    for npc in current_area.npcs:
        sprite_surface.blit(people[npc[0]], (total_offset[0] + npc[1]*TILE_SIZE, total_offset[1] + npc[2]*TILE_SIZE))
    sprite_surface.blit(player_sprite[f"{current_player_data.facing}_{stance}"], screen_center)

    sprite_surface_scaled = pygame.transform.scale(sprite_surface, current_screen_dims)
    screen.blit(sprite_surface_scaled, (0,0))
    text = font.render(f"{round(mainClock.get_fps())}, {current_player_data.get_pointing()}, ", True, (0,0,100), (100,0,0))
    screen.blit(text, (0,0))

    pygame.display.update()
    mainClock.tick(60)