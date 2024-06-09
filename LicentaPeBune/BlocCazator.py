import pygame
from Gameproperties import Properties
import random

class Block(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("img/Licenta.png")
        self.rect = self.surf.get_rect(center=(-100, -100))
        wrandom = random.randint(150, int(Properties.latime - 150))
        self.pos = Properties.vec((wrandom, 0))


    def moveblock(self):
        self.pos.y += Properties.viteza_bloc
        self.rect.midbottom = self.pos
        if self.pos.y > 800:
            Properties.running=False
