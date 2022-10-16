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
        self.surface = pygame.Surface(((15*TILE_SCALE)/2,(10*TILE_SCALE)/2))
        self.pairs = self.find_pairs()
        self.pair_nr = 0
    
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

    def scroll(self):
        awaiting_press = False
        p = 0
        if not awaiting_press:
            for i, line in enumerate(self.pairs[self.pair_nr]):
                x_offset = 0
                
                for word in line:
                    for letter in word:
                        if self.counter >= p*FRAMES_PER_LETTER:
                            self.surface.blit(letters[letter], (x_offset,i*20))
                            x_offset += letter_lengths[letter][0] + 1
                            p += 1

                #prevents counter going to infinity
                if self.counter < p*FRAMES_PER_LETTER*2:
                    self.counter += 1
                else:
                    self.counter = 0
                    self.pair_nr += 1
        
            




pygame.init()
mainClock = pygame.time.Clock()

screen = pygame.display.set_mode(((15*TILE_SCALE, 10*TILE_SCALE)), pygame.RESIZABLE)


a = Text("peepeepoopoo, I don't need a bathroom pls now yes! I HAVE TO POOP...?", 20,20)
print(a.text)
print(a.find_pairs())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    a.surface.fill((255,255,255))
    a.scroll()
    screen_scaled = pygame.transform.scale(a.surface, (15*TILE_SCALE, 10*TILE_SCALE))
    screen.blit(screen_scaled, (0,0))

    pygame.display.update()
    mainClock.tick(FRAMERATE)