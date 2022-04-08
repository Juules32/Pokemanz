import pygame
from constants import *

#displays
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode((15*TILE_SCALE, 10*TILE_SCALE), pygame.RESIZABLE)
current_screen_dims = pygame.display.get_surface().get_size()
sprite_surface = pygame.Surface((current_screen_dims[0]/SCALE_FACTOR, current_screen_dims[1]/SCALE_FACTOR))
