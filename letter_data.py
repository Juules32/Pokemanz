import pygame

letters = {}

for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,!' ":
    if letter.lower() == letter:
        letters[letter] = pygame.image.load("Assets/" + letter.lower() + ".png")
    else:
        letters[letter] = pygame.image.load("Assets/" + letter.upper() + letter.lower() + ".png")

letters["?"] = pygame.image.load("Assets/question_mark.png")


letter_lengths = {}

for key, value in letters.items():
    letter_lengths[key] = value.get_size()
