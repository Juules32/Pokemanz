import time, pygame, sys
from pygame.locals import *

from constants import *
from Classes.screen import Screen

from letter_data import letters, letter_lengths

class Text:
    def __init__(self, text, posx, posy):
        self.text = text
        self.bubble_image = pygame.image.load("Assets/Dialogue/text_box.png")
        self.bubble = pygame.transform.scale2x(self.bubble_image)
        self.surface = pygame.Surface(self.bubble.get_size(), pygame.SRCALPHA, 32).convert_alpha() #transparency
        self.pos = (posx, posy)
        self.counter = 0
        self.length = len(text)
        self.pairs = self.find_pairs()
        self.length = len(self.pairs)
        self.pair_nr = 0
        self.finished_animation = False
        self.finished_talking = False
        self.pressing = False

    def get_scaled(self):
        return pygame.transform.scale(self.surface, (self.surface.get_width()*2, self.surface.get_height()*2))
    
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
            if line_count <= 166:
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
        if not self.finished_talking:
            coefficient = 0
            self.surface.blit(self.bubble, (0,0))
            if not self.finished_animation:
                self.pressing = False

                for i, line in enumerate(self.pairs[self.pair_nr]):
                    x_offset = 0
                    
                    for word in line:
                        for letter in word:
                            if self.counter >= coefficient*FRAMES_PER_LETTER:
                                self.surface.blit(letters[letter], (14+x_offset,14+i*20))
                                x_offset += letter_lengths[letter][0] + 1 #1 is amount of pixels between letters
                                coefficient += 1
                            else:
                                break

                #prevents counter going to infinity
                if self.counter < coefficient*FRAMES_PER_LETTER:
                    self.counter += 1
                else:

                    #displays this when line finished animating
                    self.counter = 0
                    self.finished_animation = True
                    

            if self.finished_animation:

                #draw the whole pair
                for i, line in enumerate(self.pairs[self.pair_nr]):
                    x_offset = 0
                    for word in line:
                        for letter in word:
                            self.surface.blit(letters[letter], (14+x_offset,14+i*20))
                            x_offset += letter_lengths[letter][0] + 1 #1 is amount of pixels between letters

                self.surface.blit(letters["next"], (204,14+20))

                self.checkFinished()

                if self.pressing:
                    self.pressing = False
                    self.finished_animation = False
                    self.pair_nr += 1
                    print(self.length, self.pair_nr)


    def checkFinished(self):
        self.finished_talking = True if self.pair_nr + 1 >= self.length else False
