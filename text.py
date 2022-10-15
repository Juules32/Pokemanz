import time, pygame, sys
from constants import *
from Classes.displays import Screen

from letter_data import letters, letter_lengths

class Text:
    def __init__(self, text, posx, posy):
        self.text = text
        self.pos = (posx, posy)
        self.counter = 0
        self.length = len(text)
        

    def scroll(self, screen):
        offset = 10
        for i in range(self.length):
            if self.counter >= i*FRAMES_PER_LETTER:
                screen.blit(letters[self.text[i]], (offset,10))
                offset += letter_lengths[self.text[i]][0] + 1

        #prevents counter going to infinity
        if self.counter != self.length*FRAMES_PER_LETTER:
            self.counter += 1
        
            




pygame.init()
mainClock = pygame.time.Clock()

screen = pygame.display.set_mode(((15*TILE_SCALE, 10*TILE_SCALE)), pygame.RESIZABLE)

surface = pygame.Surface(((15*TILE_SCALE)/2,(10*TILE_SCALE)/2))

a = Text("peepeepoopoo, I don't need a bathroom pls now yes! I HAVE TO POOP...", 20,20)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    surface.fill((255,255,255))
    a.scroll(surface)
    screen_scaled = pygame.transform.scale(surface, (15*TILE_SCALE, 10*TILE_SCALE))
    screen.blit(screen_scaled, (0,0))

    pygame.display.update()
    mainClock.tick(FRAMERATE)