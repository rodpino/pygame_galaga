import pygame
from setting import *


class Background ():
    
    def __init__(self):        
        self.screen = pygame.display.get_surface()
        self.pos_y = 0
        self.image = pygame.image.load ("asset/bg_space2.bmp")
        self.image = pygame.transform.scale (self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.velocity = 250
                     
    def draw (self):
        self.screen.blit (self.image, (0, self.pos_y))
        self.screen.blit (self.image, (0, self.pos_y - self.rect.height))
                      
    def update (self, dt):        
        self.pos_y += self.velocity * dt
        if self.pos_y >= self.rect.height: 
            self.pos_y = 0
            
