import pygame
from constants import *

class Screen:
    def __init__(self):
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.mode = pygame.display.set_mode((15*TILE_SCALE, 10*TILE_SCALE), pygame.RESIZABLE)
        self.current_dims = pygame.display.get_surface().get_size()
        self.sprite_surface = pygame.Surface((self.current_dims[0]/SCALE_FACTOR, self.current_dims[1]/SCALE_FACTOR))

        #screen sizing variables
        self.xy = self.get_tiles_avaliable(self.current_dims)
        self.center = self.get_center()
        self.fullscreen = False
        self.stored_size = [15, 10]
        self.total_offset = None

    def get_center(self):
        return ((self.xy[0]/2 - 0.5)*TILE_SIZE, (self.xy[1]/2 - 0.5)*TILE_SIZE)

    def get_tiles_avaliable (self, dims):
        x = round(dims[0]/TILE_SCALE)
        y = round(dims[1]/TILE_SCALE)
        return (x, y)

    def size_check (self, dims, min_display_size = [9 * TILE_SCALE, 6 * TILE_SCALE]):
        w = dims[0]
        h = dims[1]
        if dims[0] < min_display_size[0]:
            w = min_display_size[0]
        if dims[1] < min_display_size[1]:
            h = min_display_size[1]    
        return (w, h)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.stored_size = self.current_dims
            self.xy = self.get_tiles_avaliable(self.monitor_size)
            self.mode = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
        else:
            self.mode = pygame.display.set_mode(self.stored_size, pygame.RESIZABLE)
        self.current_dims = (self.xy[0]*TILE_SCALE, self.xy[1]*TILE_SCALE)
        self.center = self.get_center()
        self.sprite_surface = pygame.Surface((self.current_dims[0]/SCALE_FACTOR, self.current_dims[1]/SCALE_FACTOR))

    def resize(self, event):
        if not self.fullscreen:
            self.current_dims = self.size_check((event.w, event.h))
            self.stored_size = self.current_dims
            self.xy = self.get_tiles_avaliable(self.current_dims)
            self.mode = pygame.display.set_mode(self.current_dims, pygame.RESIZABLE)
            self.center = self.get_center()
            self.sprite_surface = pygame.Surface((self.current_dims[0]/SCALE_FACTOR, self.current_dims[1]/SCALE_FACTOR))