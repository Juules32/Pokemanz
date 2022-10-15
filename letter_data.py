import pygame

letters = {}

for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,!' ":
    a = letter.lower()
    Aa = letter.upper()
    if letter == a:
        letters[letter] = pygame.image.load("Assets/" + a + ".png")
    else:
        letters[letter] = pygame.image.load("Assets/" + Aa + a + ".png")

letter_lengths = {}

for key, value in letters.items():
    letter_lengths[key] = value.get_size()

