import pygame
import time

from entities.laser import *
from debug import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = pygame.display.get_surface()
        self.lives = 3
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
        
        # atricutis rotate_palyer
        
        self.sprite = self.nave_2
        self.duration = 2
        
        self.rotation_speed = 80
        self.start_time = None
        self.elapsed_time = 0
        self.angle = 0
   
        
        self.active_rotation = False  # Indica si la rotación está activa
        
        
        
                
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
                    self.player_shoot()
                    self.last_shot_time = current_time
                    self.shots_fired += 1
                    self.laser_collided = False  # Restablecer el indicador de colisión
            elif self.shots_fired >= 2 and current_time - self.shoot_time > self.shoot_cooldown:
                self.shots_fired = 0
                self.shoot_time = current_time

    def player_shoot(self):
        laser = Laser(self.rect.center, self.game)
        self.laser_group.add(laser)
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
     
    def start(self):
        """Inicia la rotación."""
        self.start_time = time.time()
        self.active_rotation = True
        print("colisionnnnnn")

    def rotate_player(self):
        """Actualiza la rotación del sprite."""
        if not self.active_rotation:
            
            return
        print("rotacion activa")
        # Calcula el tiempo transcurrido
        self.elapsed_time = time.time() - self.start_time

        # Verifica si la animación ha finalizado
        if self.elapsed_time >= self.duration:
            self.active_rotation = False
            return

        # Calcula el ángulo actual de rotación
        self.angle += self.rotation_speed * (1 / 60)  # Aproximación para 60 FPS
        self.angle %= 360  # Asegura que el ángulo esté en [0, 360)

        # Rotar el sprite
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)

        # Recalcula el rectángulo para mantenerlo centrado
        rotated_rect = rotated_sprite.get_rect(center=self.rect.center)

        # Dibujar el sprite rotado en la pantalla
        self.screen.blit(rotated_sprite, rotated_rect.topleft)
     

    def update(self, delta_time):
        self.player_input()
        self.position.x += self.direction.x * self.velocity * delta_time
        self.rect.x = round(self.position.x)
        self.laser_group.update(delta_time)
        self.rotate_player()

    def debug(self, info, y=100, x=50):
        self.screen = pygame.display.get_surface()
        debug_surf = font.render(str(info), True, "white")
        debug_rect = debug_surf.get_rect(topleft=(x, y))
        pygame.draw.rect(self.screen, "black", debug_rect)
        self.screen.blit(debug_surf, debug_rect)

