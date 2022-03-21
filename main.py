# TODO:
#HETTTYYYY: et problem er at offset og current_data ikke fungerer sammen endnu.
# 0: walkable
# 1: walls
# 2: warps
# 3: default spawn
# 4: interactable walls
# 5: interactable ground
# 6: visible pickup
# 7: insivible pickup

#imports
import pygame, json, sys
from pygame.locals import *
from Classes.saving import *
from Classes.areas import *

#constants
TILE_SIZE = 16
SCALE_FACTOR = 4
TILE_SCALE = TILE_SIZE * SCALE_FACTOR
WALKING_SPEED = 2
RATIO = 1.5

#initialisations
pygame.init()
mainClock = pygame.time.Clock()
pygame.display.set_caption("Hello World!")
font = pygame.font.Font('freesansbold.ttf', 32)

#displays
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((15*TILE_SCALE, 10*TILE_SCALE), pygame.RESIZABLE)
current_screen_dimensions = pygame.display.get_surface().get_size()
background_surface = pygame.Surface((current_screen_dimensions[0]/SCALE_FACTOR, current_screen_dimensions[1]/SCALE_FACTOR))

#image loading
player = pygame.image.load("assets/images/Player.png")
plains_background = pygame.image.load("areas/plains/plains_background.png")
plains_collision = pygame.image.load("areas/plains/plains_collision.png")
cool_house = pygame.image.load("assets/images/cool_house.png")
sailor = pygame.image.load("assets/images/Player.png")

def get_screen_center(dimensions):
    return ((dimensions[0]/2 - 0.5)*TILE_SIZE, (dimensions[1]/2 - 0.5)*TILE_SIZE)

def find_tiles_avaliable (dimensions):
    x = round(dimensions[0]/TILE_SCALE)
    y = round(dimensions[1]/TILE_SCALE)
    return (x, y)

def size_check (dimensions, minimum_display_size = [9 * TILE_SCALE, 6 * TILE_SCALE]):
    w = dimensions[0]
    h = dimensions[1]
    if dimensions[0] < minimum_display_size[0]:
        w = minimum_display_size[0]
    if dimensions[1] < minimum_display_size[1]:
        h = minimum_display_size[1]    
    return (w, h)

def run_1_tile(direction):
    x = 0
    while x < TILE_SIZE:
        run_queue.append(direction)
        x += 1
    current_data["position"][0] += direction[0]
    current_data["position"][1] += direction[1]

#game loop variable inits
xy = find_tiles_avaliable(current_screen_dimensions)
screen_center = get_screen_center(xy)
fullscreen = False
position_offset = [0,0]
latest_direction = None
current_directions = []
stored_size = [15, 10]
run_queue = []

#read save
with open(f"save_{1}.txt") as save:
    data = json.load(save)
with open(f"save_{1}.txt") as save:
    current_data = json.load(save)

#game loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    stored_size = current_screen_dimensions
                    xy = find_tiles_avaliable(monitor_size)
                    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(stored_size, pygame.RESIZABLE)
                current_screen_dimensions = (xy[0]*TILE_SCALE, xy[1]*TILE_SCALE)
                screen_center = get_screen_center(xy)
                background_surface = pygame.Surface((current_screen_dimensions[0]/SCALE_FACTOR, current_screen_dimensions[1]/SCALE_FACTOR))
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                if event.key == K_a:
                    latest_direction = (-1, 0)
                if event.key == K_d:
                    latest_direction = (1, 0)
                if event.key == K_w:
                    latest_direction = (0, -1)
                if event.key == K_s:
                    latest_direction = (0, 1)
                current_directions.append(latest_direction)
        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d or event.key == K_w or event.key == K_s:
                if event.key == K_a:
                    current_directions.pop(current_directions.index((-1, 0)))
                if event.key == K_d:
                    current_directions.pop(current_directions.index((1, 0)))
                if event.key == K_w:
                    current_directions.pop(current_directions.index((0, -1)))
                if event.key == K_s:
                    current_directions.pop(current_directions.index((0, 1)))
        if event.type == VIDEORESIZE:
            if not fullscreen:
                current_screen_dimensions = (event.w, event.h)
                current_screen_dimensions = size_check(current_screen_dimensions)
                stored_size = current_screen_dimensions
                xy = find_tiles_avaliable(current_screen_dimensions)
                screen = pygame.display.set_mode(current_screen_dimensions, pygame.RESIZABLE)
                screen_center = get_screen_center(xy)
                background_surface = pygame.Surface((current_screen_dimensions[0]/SCALE_FACTOR, current_screen_dimensions[1]/SCALE_FACTOR))
        if event.type == QUIT:
            with open(f"save_{1}.txt", "w") as save:
                print("ee")
                json.dump(current_data, save)
            pygame.quit()
            sys.exit()

    #animation
    if len(current_directions):
        direction = current_directions[-1]

        if not len(run_queue):
            run_1_tile(direction)
            print(data, current_data)
            
        elif direction not in run_queue:
            run_1_tile(direction)

    if len(run_queue):
        direction = run_queue[0]
        position_offset[0] -= direction[0] * WALKING_SPEED
        position_offset[1] -= direction[1] * WALKING_SPEED
        run_queue = run_queue[WALKING_SPEED:]
        
    rounded_offset = [int(position_offset[0]), int(position_offset[1])]

    #rendering
    background_surface.fill((20,20,20))
    background_surface.blit(plains_background,  (rounded_offset[0] + screen_center[0] - data["position"][0]*TILE_SIZE, rounded_offset[1] + screen_center[1] - data["position"][1]*TILE_SIZE))
    background_surface.blit(cool_house,  (rounded_offset[0] + screen_center[0] - data["position"][0]*TILE_SIZE, rounded_offset[1] + screen_center[1] - data["position"][1]*TILE_SIZE))
    background_surface.blit(player, screen_center)

    background_surface_scaled = pygame.transform.scale(background_surface, current_screen_dimensions)
    screen.blit(background_surface_scaled, (0,0))
    text = font.render(f"{round(mainClock.get_fps())}, {current_directions}, {position_offset}, ", True, (0,0,100), (100,0,0))
    screen.blit(text, (0,0))

    pygame.display.update()
    mainClock.tick(60)