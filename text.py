import time, pygame, sys
from pygame.locals import *

from constants import *
from Classes.displays import Screen

from letter_data import letters, letter_lengths

class Text:
    def __init__(self, text, posx, posy, surface):
        self.text = text
        self.bubble = text_box = pygame.image.load("Assets/Dialogue/text_box.png")
        self.pos = (posx, posy)
        self.counter = 0
        self.length = len(text)
        self.pairs = self.find_pairs()
        self.length = len(self.pairs)
        self.pair_nr = 0
        self.awaiting_press = False
        self.surface = surface
    
    def find_pairs(self):
        
        #lines are sorted into pairs because up to two lines of text can be displayed
        pairs = []

        lines = []
        current_line = []
        
        #used for keeping track of how long each line is
        line_count = 0

        #iterates over each word of the input text
        for word in self.text.split(" "):

            #used for keeping track of how long each word is
            word_count = 0

            #increments line_count by the length of each letter's image width
            for letter in word:
                word_count += letter_lengths[letter][0]
            line_count += word_count + letter_lengths[" "][0]
            
            #if line_count is under 180 pixels, adds word to current line
            if line_count <= 180:
                current_line.append(word + " ")

            #otherwise, current_line is added to lines, and variables are set to current word, since it didn't make it into current_line
            else:
                lines.append(current_line)
                current_line = [word + " "]
                line_count = word_count + letter_lengths[" "][0]

        #the last current_line is added to lines
        lines.append(current_line)

        #every two lines are grouped into pairs
        for i in range(0, len(lines), 2):
            pee = [lines[i]]
            if i + 1 < len(lines):
                pee.append(lines[i+1])
            pairs.append(pee)
        return pairs

    def scroll(self, x, y, pressing = False):
        coefficient = 0
        if not self.awaiting_press:
            for i, line in enumerate(self.pairs[self.pair_nr]):
                x_offset = 0
                self.surface.blit(self.bubble, (x,y))
                
                for word in line:
                    for letter in word:
                        if self.counter >= coefficient*FRAMES_PER_LETTER:
                            self.surface.blit(letters[letter], (x+x_offset,y+i*20))
                            x_offset += letter_lengths[letter][0] + 1 #1 is amount of pixels between letters
                            coefficient += 1

                #prevents counter going to infinity
                if self.counter < coefficient*FRAMES_PER_LETTER*2:
                    self.counter += 1
                else:
                    self.counter = 0
                    self.awaiting_press = True
                    break

        
        if self.awaiting_press:
            for i, line in enumerate(self.pairs[self.pair_nr]):
                x_offset = 0
                for word in line:
                    for letter in word:
                        self.surface.blit(letters[letter], (x_offset,i*20))
                        x_offset += letter_lengths[letter][0] + 1 #1 is amount of pixels between letters
                            
            if pressing:
                print("pla")
                self.awaiting_press = False
                if self.pair_nr + 1 < self.length:
                    self.pair_nr += 1
                else:
                    print("done")


pygame.init()
mainClock = pygame.time.Clock()

screen = pygame.display.set_mode(((15*TILE_SCALE, 10*TILE_SCALE)), pygame.RESIZABLE)

a = None

while True:
    pressing = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_z:
                pressing = True
                a = Text("Hello! My name is Michael McDingus, and I'll be your trainer", 20, 20, screen)



    if a != None:
        a.scroll(pressing, 20, 20)
        screen_scaled = pygame.transform.scale(a.surface, (15*TILE_SCALE, 10*TILE_SCALE))
        screen.blit(screen_scaled, (0,0))

    pygame.display.update()
    mainClock.tick(FRAMERATE)