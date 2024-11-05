import pygame

from entities.laser import Laser
from debug import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x=None, y=None):
        super().__init__()
        self.game = game
        
        self.screen = pygame.display.get_surface()
        self.lives = 1
        self.laser_group = pygame.sprite.Group()
        self.sprite_sheet = pygame.image.load("asset/Galaga_SpritesSheet.png").convert_alpha()
        self.nave_1 = self.sprite_sheet.subsurface(109, 1, self.game.settings.SPRITE_SIZE, self.game.settings.SPRITE_SIZE)
        self.nave_2 = self.sprite_sheet.subsurface(109, 19, self.game.settings.SPRITE_SIZE, self.game.settings.SPRITE_SIZE)
        self.nave_1 = pygame.transform.scale(self.nave_1, (self.game.settings.PLAYER_SIZE)) 
        self.nave_2 = pygame.transform.scale(self.nave_2, (self.game.settings.PLAYER_SIZE)) 
        self.index = 0

        self.image = self.nave_1
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(self.game.settings.WIDTH / 2, self.game.settings.HEIGHT - 95))
        if x is not None and y is not None:
            self.rect.center = (x, y)
        else:
            self.rect.center = (self.game.settings.WIDTH / 2, self.game.settings.HEIGHT - 95)
        
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.velocity = 380
        self.shoot_ready = True
        self.shoot_cooldown = 800  # Tiempo de enfriamiento entre ráfagas
        self.shoot_time = 0
        self.shots_fired = 0  # Contador de disparos en la ráfaga
        self.rafaga_cooldown = 200  # Pausa entre los dos disparos de la ráfaga
        self.last_shot_time = 0
        self.laser_collided = False  # Indicador de colisión del láser
        self.sound_shoot = pygame.mixer.Sound ("asset/sound_shoot_3.wav")
        self.mask = pygame.mask.from_surface(self.image)
        self.has_clone = False
    
    def player_input(self):
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if self.keys[pygame.K_RIGHT] and self.rect.right < self.game.settings.WIDTH:
            self.direction.x = 1
        elif self.keys[pygame.K_LEFT] and self.rect.left > 0:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if self.keys[pygame.K_SPACE]:
            
            if self.shots_fired < 2:
                if current_time - self.last_shot_time > self.rafaga_cooldown or self.laser_collided:
                    
                    for player in self.game.player_group:
                        
                        
                        self.shoot()
                        self.last_shot_time = current_time
                        self.shots_fired += 1
                        self.laser_collided = False  # Restablecer el indicador de colisión
            elif self.shots_fired >= 2 and current_time - self.shoot_time > self.shoot_cooldown:
                self.shots_fired = 0
                self.shoot_time = current_time

    def shoot(self):
        laser = Laser(self.game, (self.rect.centerx, self.rect.top))
        self.laser_group.add(laser)
        self.game.player_lasers.add(laser)  # Agregar al grupo global
            
        #self.sound_shoot.play()
    
    
    
    def draw_life_player(self):
        """dibuja vidas del player"""
        for i in range(self.lives):
            self.nave_1 = pygame.transform.scale(self.nave_1, (25 , 25))
            
            x = 10 + i * (self.nave_1.get_width() + 5)
            y = self.game.settings.HEIGHT - 30
            self.screen.blit(self.nave_1, (x, y))
            
        if self.lives == 0 or len(self.game.formation.aliens) == 0:
            self.game.resources.game_over()  # Llama a la función para mostrar el texto "Game Over"
                    
    def update(self, delta_time):
        self.player_input()
        self.position.x += self.direction.x * self.velocity * delta_time
        self.rect.x = round(self.position.x)
        self.laser_group.update(delta_time)
        
        # Debugging the player state
        # self.debug(f"Shots fired: {self.shots_fired}", 10, 10)
        # self.debug(f"Shoot cooldown: {self.shoot_cooldown}", 30, 10)
        # self.debug(f"Laser collided: {self.laser_collided}", 50, 10)

    def debug(self, info, y=100, x=50):
        self.screen = pygame.display.get_surface()
        debug_surf = font.render(str(info), True, "white")
        debug_rect = debug_surf.get_rect(topleft=(x, y))
        pygame.draw.rect(self.screen, "black", debug_rect)
        self.screen.blit(debug_surf, debug_rect)
