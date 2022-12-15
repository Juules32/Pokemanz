# gør current_location til et felt i player klassen, evt ved at adskille entity til npc og player, så der ikke er circular references.
#lav "Map" over sammenspil mellem klasser, for at skabe lavere kobling. Der skal helst ske så få udregninger, som muligt i main klassen.
# Can't move when speaking. player.interacting i stedet for interactible.interacting
# Implementér running
# lav * " og : i pixel art
# i subclassen ImportantNpc i Npc.py så skal de kunne bevæge sig, være i koreograferede cutscener, etc.
# Genovervej, hvordan du vil strukturere maps

#removes "Hello from the pygame community..." from terminal
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame, json, sys
from pygame.locals import *
from constants import *
from Classes.screen import Screen
from Classes.map import Map
from text import Text
from Classes.entity import Player, Npc, ImportantNpc, Item, Entity

#initializations
pygame.init()
pygame.display.set_icon(pygame.image.load("Assets/Icons/icon.png"))
pygame.display.set_caption("Pokémanz!")
mainClock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

areas = {
    "plains": Map("plains")
}



#Instantiating important classes
screen = Screen()
plains = Map("plains")
player = Player("Player_1", "plains", (1,1))
player.load()



player.pos_offset = [player.pos[0]*TILE_SIZE, player.pos[1]*TILE_SIZE]

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
                screen.toggle_fullscreen()
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
            screen.resize(event)
        if event.type == QUIT:
            player.save()
            pygame.quit()
            sys.exit()

    #animation
    player.animate()
    
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
    screen.total_offset = (-player.pos_offset[0] + screen.center[0], -player.pos_offset[1] + screen.center[1])
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
    

    screen.sprite_surface_scaled = pygame.transform.scale(screen.sprite_surface, screen.current_dims)

    if not isinstance(object_looked_at, int):
        if object_looked_at.interacting:
            object_looked_at.dialogue.scroll()
            screen.sprite_surface_scaled.blit(object_looked_at.dialogue.get_scaled(), (screen.center[0]*4 - object_looked_at.dialogue.bubble.get_width()*2/2 + player.facing[0]*TILE_SIZE*4 + TILE_SCALE/2, (screen.center[1] - TILE_SIZE*0.5)*4 + player.facing[1]*TILE_SIZE*4 - TILE_SCALE*2 - TILE_SCALE*0.25))
        else:
            object_looked_at.dialogue = None
    
    screen.mode.blit(screen.sprite_surface_scaled, (0,0))
    text = font.render(f"{round(mainClock.get_fps())}, {player.get_pointing()}, {player.facing}", True, (0,0,100), (100,0,0))
    screen.mode.blit(text, (0,0))

    pygame.display.update()
    mainClock.tick(FRAMERATE)