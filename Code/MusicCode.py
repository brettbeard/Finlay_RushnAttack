
import pygame

def MusicPlayer():

    pygame.mixer.music.load("../Sounds/Stage1Theme.mp3")
    pygame.mixer.music.play(-1)
