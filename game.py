
import pygame
import sys
import time
import os

from settings import Settings
from entities.player import Player
from entities.laser import Laser
from entities.explosion import Explosion
from entities.attack_curves_relativas import Curvas_relativas
from entities.background import Background
from entities.formation import Formation
from entities.alien import Alien
from utils.resources import Resources
from entities.capture_light import CaptureLight



class Game():

    def __init__(self):
        # Inicializar Pygame y configuraciones
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption("Galaga Pygame")

        # Inicializar componentes del juego
        self.resources = Resources(self)
        self.background = Background(self)
        
        self.formation = Formation(self)
        self.explosion_size = (70, 70)
        self.explosion = Explosion(self)
        self.explosion_group = pygame.sprite.Group()
        #self.explosion_group.add(self.explosion)
        # Player Setup
        self.player = Player(self)
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)
        self.hit_count = 0
        
        self.capture_light = CaptureLight(self, 400, 600)
        self.capture_light_group = pygame.sprite.Group(self.capture_light)
        # Puntaje
        self.score = 0  # Iniciar el puntaje en 0
        self.high_score = self.resources.load_high_score()
         # Fuente para mostrar el puntaje
        self.FONT_score = pygame.font.Font('asset/fonts/emulogic.ttf', 20)

        # Fuente para mostrar el mIndex
        self.FONT = pygame.font.SysFont(None, 30)
        self.font = pygame.font.Font("asset/fonts/emulogic.ttf", 8)

        # Fuente para mostrar el puntaje
        self.FONT_score = pygame.font.Font('asset/fonts/emulogic.ttf', 20)
        self.clock = pygame.time.Clock()
    
    def draw_capture(self, delta_time):
        self.capture_light.update(delta_time)
        CaptureLight.sprite_animation(delta_time)
        print("capture ???")
        # Actualizar la imagen del sprite usando el índice global de animación
        
    
        # Actualiza la posición del sprite en la pantalla
        self.rect = self.formation.aliens.x, self.formation.alien.y
        self.screen.blit(self.capture_light.image, self.rect)
        
    def calculate_delta_time(self) -> float:
        """Calcula y devuelve el delta_time usando time.time()"""

        # Inicializa `self.last_time` la primera vez que se llama a la función
        if not hasattr(self, "last_time"):
            self.last_time = time.time()

        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time  # Actualiza `last_time` para el próximo ciclo
        return delta_time

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.resources.save_high_score()
                self.running = False

    def update_game_state(self, delta_time):
        self.formation.update(delta_time)
        self.background.update(delta_time)
        self.player_group.update(delta_time)
        self.resources.check_for_collision()
        self.explosion.update(delta_time)
        self.resources.check_high_score()  # Verificar si el score actual supera el high score
        for alien_sprite in self.formation.aliens:
            alien_sprite.laser_group.update(delta_time)
        Alien.sprite_animation(delta_time)
        self.capture_light_group.update(delta_time)
    def render(self, fps, delta_time):
        self.screen.fill(self.settings.BLACK)
        self.background.draw()
        self.formation.draw(self.screen, delta_time)
        self.player_group.draw(self.screen)
        self.player.laser_group.draw(self.screen)
        self.resources.draw_score()
        self.player.draw_life_player()
        self.explosion_group.draw(self.screen)
        self.resources.show_fps(fps)
        for alien_sprite in self.formation.aliens:
            alien_sprite.laser_group.draw(self.screen)
        self.capture_light_group.draw(self.screen)
        #self.resources.draw_bezier_path(self.screen)
        #self.resources.debug(len(self.explosion_group))
        pygame.display.flip()

    def run(self):
        # Bucle principal del juego
        self.running = True
        delta_time = self.calculate_delta_time()
        
        while self.running:
            delta_time = self.calculate_delta_time()
            fps = self.clock.get_fps()
            self.clock.tick()
            self.handle_events()
            self.update_game_state(delta_time)
            
            self.render(fps, delta_time)
            
        # Salir de Pygame
        pygame.quit()
        sys.exit()
