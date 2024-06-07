import pygame
from pygame.locals import *
from Gameproperties import Properties


class Platform(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/BodoRemastered.png")
        self.rect = self.surf.get_rect(center=(Properties.latime/2, Properties.inaltime))
        self.pos = Properties.vec((Properties.latime / 2, Properties.inaltime))

    # move: This method moves the platform left or right based on the pressed keys. For the game played by human.

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.pos.x -= Properties.viteza_platforma
        if pressed_keys[K_RIGHT]:
            self.pos.x += Properties.viteza_platforma

        if self.pos.x > Properties.latime - 100:
            self.pos.x = Properties.latime - 100
        if self.pos.x < 100:
            self.pos.x = 100
        self.rect.midbottom = self.pos

    def move_left(self):
        self.pos.x -= Properties.viteza_platforma
        if self.pos.x < 100:
            self.pos.x = 100
        self.rect.midbottom = self.pos

    def move_right(self):
        self.pos.x += Properties.viteza_platforma
        if self.pos.x > Properties.latime - 100:
            self.pos.x = Properties.latime - 100
        self.rect.midbottom = self.pos

    def stay_in_place(self):
        self.rect.midbottom = self.pos

# 2. „from pygame.locals import *” importă un set de constante din librăria Pygame, în cazul jocului nostru este folosit pentru mișcarea platformei stânga-dreapta.