import pygame


class Laser (pygame.sprite.Sprite):

    def __init__(self, position, game):
        super().__init__()
        self.game = game
        self.position = position
        self.screen = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load("asset/Galaga_SpritesSheet.png").convert_alpha()        
        self.image = self.sprite_sheet.subsurface(307, 118, self.game.settings.SPRITE_SIZE, self.game.settings.SPRITE_SIZE)
        self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.image.set_colorkey(self.game.settings.BLACK)
        self.rect = self.image.get_rect(center=self.position)
        self.position = pygame.math.Vector2(self.rect.midtop)
        self.direction = pygame.math.Vector2()
        self.velocity = 180
        self.direction.y = -4        

        # Generar la máscara para el láser
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.screen.blit(self.image, self.rect)
 
    def update(self, delta_time):
        self.position.y += self.direction.y * self.velocity * delta_time
        self.rect.y = round(self.position.y)
        if self.rect.y < -10:
            self.kill()
