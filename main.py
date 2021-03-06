# TODO:

#imports
from asyncio.windows_events import NULL
from operator import index
import pygame, json, sys

#initializations
pygame.init()
pygame.display.set_caption("Pokémanz!")
mainClock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

from constants import *
from displays import *
from pygame.locals import *
from Classes.areas import *
from Classes.player import *

#read save
with open(f"Save Data/save_{1}.txt") as save:
    data = json.load(save)
    for key, value in data.items():
        setattr(player, key, value)
save.close()

screen.pos_offset = [player.pos[0]*TILE_SIZE, player.pos[1]*TILE_SIZE]

#current area
current_area = plains

#game loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_z:
                player.wants_to_interact = True
            if event.key == K_f:
                screen.fullscreen = not screen.fullscreen
                if screen.fullscreen:
                    screen.stored_size = screen.current_dims
                    screen.xy = screen.get_tiles_avaliable(screen.monitor_size)
                    screen.mode = pygame.display.set_mode(screen.monitor_size, pygame.FULLSCREEN)
                else:
                    screen.mode = pygame.display.set_mode(screen.stored_size, pygame.RESIZABLE)
                screen.current_dims = (screen.xy[0]*TILE_SCALE, screen.xy[1]*TILE_SCALE)
                screen.center = screen.get_center()
                screen.sprite_surface = pygame.Surface((screen.current_dims[0]/SCALE_FACTOR, screen.current_dims[1]/SCALE_FACTOR))
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                if event.key == K_a:
                    player.latest_dir = (-1, 0)
                if event.key == K_d:
                    player.latest_dir = (1, 0)
                if event.key == K_w:
                    player.latest_dir = (0, -1)
                if event.key == K_s:
                    player.latest_dir = (0, 1)
                player.current_dirs.append(player.latest_dir)
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                if event.key == K_a:
                    player.current_dirs.pop(player.current_dirs.index((-1, 0)))
                if event.key == K_d:
                    player.current_dirs.pop(player.current_dirs.index((1, 0)))
                if event.key == K_w:
                    player.current_dirs.pop(player.current_dirs.index((0, -1)))
                if event.key == K_s:
                    player.current_dirs.pop(player.current_dirs.index((0, 1)))
        if event.type == VIDEORESIZE:
            if not screen.fullscreen:
                screen.current_dims = screen.size_check((event.w, event.h))
                screen.stored_size = screen.current_dims
                screen.xy = screen.get_tiles_avaliable(screen.current_dims)
                screen.mode = pygame.display.set_mode(screen.current_dims, pygame.RESIZABLE)
                screen.center = screen.get_center()
                screen.sprite_surface = pygame.Surface((screen.current_dims[0]/SCALE_FACTOR, screen.current_dims[1]/SCALE_FACTOR))
        if event.type == QUIT:
            with open("Save Data/save_1.txt", "w") as save:
                data_to_be_saved = ["location", "pos", "facing", "inventory"]
                save_data = {}
                for attr, value in player.__dict__.items():
                    for data in data_to_be_saved:
                        if data == attr:
                            save_data[attr] = value
                json.dump(save_data, save)
            pygame.quit()
            sys.exit()

    #animation
    if len(player.run_queue):
        dir = player.run_queue[0]
        player.facing = [dir[0], dir[1]]
        screen.pos_offset[0] += dir[0] * WALKING_SPEED
        screen.pos_offset[1] += dir[1] * WALKING_SPEED
        length = len(player.run_queue)
        if length % TILE_SIZE == 0:
            player.count += 1
            player.stance = player.count % 2 + 1
        elif length % TILE_SIZE == 8:
            player.stance = 0
        player.run_queue = player.run_queue[WALKING_SPEED:]
    else:
        player.count = 0
        player.stance = 0

    if player.interacting:

        #interacting false when all text has been clicked through
        player.interacting = False

    else:
        #checking if player wants to interact
        if player.wants_to_interact:
            player.wants_to_interact = False
            looking_at = player.get_pointing()
            if isinstance(current_area.complete_collision[looking_at[1]][looking_at[0]], str):
                npcs["sailor1"].interact()
                player.interacting = True
        #checking if player can move
        if len(player.current_dirs):
            dir = player.current_dirs[-1]
            wants_to_go = [player.pos[0] + dir[0], player.pos[1] + dir[1]]
            if wants_to_go[0] < current_area.w and wants_to_go[0] >= 0 and wants_to_go[1] < current_area.h and wants_to_go[1] >= 0:
                if current_area.complete_collision[wants_to_go[1]][wants_to_go[0]] == 0:
                    if not len(player.run_queue):
                        player.run_1_tile(dir)
                    # never two steps from 1 input and never more than two in queue
                    elif dir not in player.run_queue and len(player.run_queue) < 16:
                        player.run_1_tile(dir)
            if not len(player.run_queue):
                player.facing = [dir[0], dir[1]]
            
        #rendering
        screen.total_offset = (-screen.pos_offset[0] + screen.center[0], -screen.pos_offset[1] + screen.center[1])
        screen.sprite_surface.fill((20,20,20))
        screen.sprite_surface.blit(current_area.background_sprite, screen.total_offset)
        screen.sprite_surface.blit(current_area.foreground_sprite, screen.total_offset)
        for npc in current_area.npcs:
            screen.sprite_surface.blit(npcs[npc[0]].sprite, (screen.total_offset[0] + npc[1]*TILE_SIZE, screen.total_offset[1] + npc[2]*TILE_SIZE))
        screen.sprite_surface.blit(player.sprites[f"{player.facing}_{player.stance}"], screen.center)
        screen.sprite_surface_scaled = pygame.transform.scale(screen.sprite_surface, screen.current_dims)
        screen.mode.blit(screen.sprite_surface_scaled, (0,0))
        text = font.render(f"{round(mainClock.get_fps())}, {player.get_pointing()}", True, (0,0,100), (100,0,0))
        screen.mode.blit(text, (0,0))

    pygame.display.update()
    mainClock.tick(60)