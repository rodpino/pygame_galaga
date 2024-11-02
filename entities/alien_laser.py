import pygame
import random


class AlienLaser(pygame.sprite.Sprite):
    def __init__(self, alien_position, player_position, game, error_margin=225):
        super().__init__()
        self.game = game
        self.position = pygame.math.Vector2(alien_position)
        self.screen = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load("asset\Galaga_SpritesSheet.png").convert_alpha()
        self.image = self.sprite_sheet.subsurface(307, 136, self.game.settings.SPRITE_SIZE, self.game.settings.SPRITE_SIZE)
        self.image = pygame.transform.scale(self.image, (30, 30)) 
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=alien_position)
       
        # Calcular la dirección hacia el jugador con variación
        player_vector = pygame.math.Vector2(player_position)
        
        # Aplicar la variación aleatoria
        if error_margin > 0:
            player_vector.x += random.uniform(-error_margin, error_margin)
            player_vector.y += random.uniform(-error_margin, error_margin)
        
        self.direction = (player_vector - self.position).normalize()
        self.velocity = 300

    def draw(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, delta_time):
        self.position += self.direction * self.velocity * delta_time
        self.rect.center = self.position
        if self.rect.y > self.game.settings.HEIGHT or self.rect.y < 0 or self.rect.x > self.game.settings.WIDTH or self.rect.x < 0:
            self.kill()
