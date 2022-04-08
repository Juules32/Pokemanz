# TODO:

#imports
from asyncio.windows_events import NULL
import pygame, json, sys, math
from initialisations import *
from constants import *
from displays import *
from pygame.locals import *
from Classes.areas import *
from Classes.player import *

#image loading
people = {
    "sailor1": pygame.image.load("Assets/sailor1.png")
}

player_sprite = {
    "[-1, 0]_0": pygame.image.load("Assets/left_0.png"),
    "[-1, 0]_1": pygame.image.load("Assets/left_1.png"),
    "[-1, 0]_2": pygame.image.load("Assets/left_2.png"),
    "[1, 0]_0": pygame.image.load("Assets/right_0.png"),
    "[1, 0]_1": pygame.image.load("Assets/right_1.png"),
    "[1, 0]_2": pygame.image.load("Assets/right_2.png"),
    "[0, -1]_0": pygame.image.load("Assets/up_0.png"),
    "[0, -1]_1": pygame.image.load("Assets/up_1.png"),
    "[0, -1]_2": pygame.image.load("Assets/up_2.png"),
    "[0, 1]_0": pygame.image.load("Assets/down_0.png"),
    "[0, 1]_1": pygame.image.load("Assets/down_1.png"),
    "[0, 1]_2": pygame.image.load("Assets/down_2.png")
}

def get_screen_center(dims):
    return ((dims[0]/2 - 0.5)*TILE_SIZE, (dims[1]/2 - 0.5)*TILE_SIZE)

def get_tiles_avaliable (dims):
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


#read save
with open(f"Save Data/save_{1}.txt") as save:
    data = json.load(save)
    for key, value in data.items():
        setattr(player, key, value)
save.close()

#screen sizing variables
xy = get_tiles_avaliable(current_screen_dims)
screen_center = get_screen_center(xy)
fullscreen = False
stored_size = [15, 10]
pos_offset = [player.pos[0]*TILE_SIZE,player.pos[1]*TILE_SIZE]
total_offset = None

#moving variables
latest_dir = None
current_dirs = []

#animation variables
count = 0
stance = 0
wants_to_interact = False
interacting = False

#current area
current_area = plains

#game loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_z:
                wants_to_interact = True
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    stored_size = current_screen_dims
                    xy = get_tiles_avaliable(monitor_size)
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
                xy = get_tiles_avaliable(current_screen_dims)
                screen = pygame.display.set_mode(current_screen_dims, pygame.RESIZABLE)
                screen_center = get_screen_center(xy)
                sprite_surface = pygame.Surface((current_screen_dims[0]/SCALE_FACTOR, current_screen_dims[1]/SCALE_FACTOR))
        if event.type == QUIT:
            with open(f"Save Data/save_{1}.txt", "w") as save:
                json.dump(player.__dict__, save)
            pygame.quit()
            sys.exit()


    #animation
    if len(player.run_queue):
        dir = player.run_queue[0]
        player.facing = [dir[0], dir[1]]
        pos_offset[0] += dir[0] * WALKING_SPEED
        pos_offset[1] += dir[1] * WALKING_SPEED
        length = len(player.run_queue)
        if length % TILE_SIZE == 0:
            count += 1
            stance = count % 2 + 1
        elif length % TILE_SIZE == 8:
            stance = 0
        player.run_queue = player.run_queue[WALKING_SPEED:]
    else:
        count = 0
        stance = 0

    

    
    if interacting:

        #interacting false when all text has been clicked through
        interacting = False

    else:
        #checking if player wants to interact
        if wants_to_interact:
            wants_to_interact = False
            looking_at = player.get_pointing()
            if isinstance(current_area.complete_collision[looking_at[1]][looking_at[0]], str):
                npcs["sailor1"].interact()
                interacting = True
        #checking if player can move
        if len(current_dirs):
            dir = current_dirs[-1]
            wants_to_go = [player.pos[0] + dir[0], player.pos[1] + dir[1]]
            if wants_to_go[0] < current_area.w and wants_to_go[0] >= 0 and wants_to_go[1] < current_area.h and wants_to_go[1] >= 0:
                if current_area.complete_collision[wants_to_go[1]][wants_to_go[0]] == 0:
                    if not len(player.run_queue):
                        player.run_1_tile(dir)
                    # never two steps from 1 input and never more than two in queue
                    elif dir not in player.run_queue and len(player.run_queue) <= 16:
                        player.run_1_tile(dir)
                else:
                    player.facing = [dir[0], dir[1]]
            else:
                player.facing = [dir[0], dir[1]]

        #rendering
        total_offset = (-pos_offset[0] + screen_center[0], -pos_offset[1] + screen_center[1])
        sprite_surface.fill((20,20,20))
        sprite_surface.blit(current_area.background_sprite, total_offset)
        sprite_surface.blit(current_area.foreground_sprite, total_offset)
        for npc in current_area.npcs:
            sprite_surface.blit(people[npc[0]], (total_offset[0] + npc[1]*TILE_SIZE, total_offset[1] + npc[2]*TILE_SIZE))
        sprite_surface.blit(player_sprite[f"{player.facing}_{stance}"], screen_center)

        sprite_surface_scaled = pygame.transform.scale(sprite_surface, current_screen_dims)
        screen.blit(sprite_surface_scaled, (0,0))
        text = font.render(f"{round(mainClock.get_fps())}, {player.get_pointing()}", True, (0,0,100), (100,0,0))
        screen.blit(text, (0,0))

    
    

    pygame.display.update()
    mainClock.tick(60)