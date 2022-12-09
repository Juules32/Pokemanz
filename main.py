# 
# How to scale dialogue properly
# How to end conversation (applies to real life as well) 
# Implementér running
# lav * " og : i pixel art
# i subclassen ImportantNpc i Npc.py så skal de kunne bevæge sig, være i koreograferede cutscener, etc.
# Genovervej, hvordan du vil strukturere maps

#removes "Hello from the pygame community..." from terminal
from asyncio.windows_events import NULL
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, json, sys

#initializations
pygame.init()
pygame.display.set_icon(pygame.image.load("Assets/Icons/icon.png"))
pygame.display.set_caption("Pokémanz!")
mainClock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

from pygame.locals import *
from constants import *
from Classes.displays import Screen
from Classes.areas import Map
from text import Text
from Classes.entities import Player, Npc, ImportantNpc, Item, Entity

screen = Screen()
plains = Map("plains")
player = Player("Player_1", "plains", (1,1))

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
    player.wants_to_interact = False

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
            if event.key == K_a:
                player.current_dirs.pop(player.current_dirs.index((-1, 0)))
            elif event.key == K_d:
                player.current_dirs.pop(player.current_dirs.index((1, 0)))
            elif event.key == K_w:
                player.current_dirs.pop(player.current_dirs.index((0, -1)))
            elif event.key == K_s:
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
    
    #checking if player can move
    if len(player.current_dirs):
        dir = player.current_dirs[-1]
        wants_to_go = [player.pos[0] + dir[0], player.pos[1] + dir[1]]
        if wants_to_go[0] < current_area.w and wants_to_go[0] >= 0 and wants_to_go[1] < current_area.h and wants_to_go[1] >= 0:
            if current_area.collision_map[wants_to_go[1]][wants_to_go[0]] == 0:
                if not len(player.run_queue):
                    player.run_1_tile(dir)
                # never two steps from 1 input and never more than two in queue
                elif dir not in player.run_queue and len(player.run_queue) < TILE_SIZE:
                    player.run_1_tile(dir)
        if not len(player.run_queue):
            player.facing = [dir[0], dir[1]]
        
    #rendering
    screen.total_offset = (-screen.pos_offset[0] + screen.center[0], -screen.pos_offset[1] + screen.center[1])
    screen.sprite_surface.fill((20,20,20))
    screen.sprite_surface.blit(current_area.background_sprite, screen.total_offset)
    screen.sprite_surface.blit(current_area.foreground_sprite, screen.total_offset)
    for i, row in enumerate(current_area.collision_map):
        if i == player.pos[1]:
            screen.sprite_surface.blit(player.sprites[f"{player.facing}_{player.stance}"], (screen.center[0], screen.center[1] - TILE_SIZE*0.5))

        for item in row:
            if not isinstance(item, int):
                screen.sprite_surface.blit(item.sprite, (screen.total_offset[0] + item.pos[0]*TILE_SIZE, screen.total_offset[1] + item.pos[1]*TILE_SIZE - TILE_SIZE*0.5))


    looking_at = player.get_pointing()
    object_looked_at = current_area.collision_map[looking_at[1]][looking_at[0]]

    #if player looking at interactible and z is pressed
    if not isinstance(object_looked_at, int) and player.wants_to_interact:
        object_looked_at.interact()
        object_looked_at.interacting = True
    
    

    screen.sprite_surface_scaled = pygame.transform.scale(screen.sprite_surface, screen.current_dims)

    if not isinstance(object_looked_at, int) and object_looked_at.interacting:
        object_looked_at.dialogue.scroll()
        screen.sprite_surface_scaled.blit(object_looked_at.dialogue.surface, (object_looked_at.pos[0]*TILE_SCALE, object_looked_at.pos[1]*TILE_SCALE))

    
    screen.mode.blit(screen.sprite_surface_scaled, (0,0))
    text = font.render(f"{round(mainClock.get_fps())}, {player.get_pointing()}", True, (0,0,100), (100,0,0))
    screen.mode.blit(text, (0,0))

    pygame.display.update()
    mainClock.tick(FRAMERATE)