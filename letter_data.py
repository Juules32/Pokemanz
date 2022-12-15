import pygame

letters = {}

for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,!'":
    if letter.lower() == letter:
        letters[letter] = pygame.image.load("Assets/Letters/" + letter.lower() + ".png")
    else:
        letters[letter] = pygame.image.load("Assets/Letters/" + letter.upper() + letter.lower() + ".png")

letters["?"] = pygame.image.load("Assets/Letters/question_mark.png")
letters[" "] = pygame.image.load("Assets/Letters/_.png")
letters["next"] = pygame.image.load("Assets/Letters/next.png")


letter_lengths = {}

for key, value in letters.items():
    letter_lengths[key] = value.get_size()
