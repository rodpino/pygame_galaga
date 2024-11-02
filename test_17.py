

import pygame
import sys
import os
import numpy as np
import random
import time
from settings import Settings
from entities.player import Player
from entities.laser import Laser
from entities.explosion import Explosion
from debug import debug_2
from entities.alien_laser import AlienLaser
from entities.capture_player import CapturePlayer
from entities.attack_curves_relativas import *
from entities.background import Background

# test github 2.1


# Clase Game
class Game:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()

        # Configuración de la ventana
        self.settings = Settings()
        self.explosion_size = (70, 70)
        self.SCREEN = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption("Pygame Galaga")
        self.sprite_explotion_coord = [(289, 1, 32, 32), (323, 1, 32, 32), (357, 1, 32, 32), (391, 1, 32, 32), (425, 1, 32, 32)]

        # Puntaje
        self.score = 0  # Iniciar el puntaje en 0
        self.high_score = self.load_high_score()
        
        # Fuente para mostrar el puntaje
        self.FONT_score = pygame.font.Font('asset/fonts/emulogic.ttf', 20)

        # Fuente para mostrar el mIndex
        self.FONT = pygame.font.SysFont(None, 30)
        self.font = pygame.font.Font("asset/fonts/emulogic.ttf", 8)
        # Cargar la hoja de sprites con la ruta actualizada
        self.SPRITE_SHEET = pygame.image.load(r"E:\Python Pygame\Python Test_6\asset\Galaga_SpritesSheet.png")
        
        self.background = Background(self)

        # Player Setup
        self.player_group = pygame.sprite.GroupSingle()
        self.player_sprite = Player(self)
        self.player_group.add(self.player_sprite)
        self.hit_count = 0
        # Crear la formación de alienígenas
        self.formation = Formation(self)
        # Explosion Setup
        self.explosion_group = pygame.sprite.Group()
        

        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()

    def get_sprite(self, coordinates):
        """Extrae el sprite de la hoja de sprites dado un rectángulo de coordenadas."""
        x, y, width, height = coordinates
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.SPRITE_SHEET, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        sprite = sprite.convert_alpha()
        return pygame.transform.scale(sprite, (40, 40))
    
    def check_for_collision(self):
        for laser_sprite in self.player_group.sprite.laser_group:
            # Verificar colisiones usando pygame.sprite.collide_mask
            collisions = pygame.sprite.spritecollide(laser_sprite, self.formation.aliens, False, pygame.sprite.collide_mask)

            for alien in collisions:
                alien.on_laser_hit()  # Llamar al método para manejar el impacto del láser
                alien_type = alien.alien_type
                
                # Manejar las colisiones
                if alien.alien_type == "boss_blue" and alien.hit_count == 2:
                    # Si es el segundo impacto, eliminar el alien
                    alien.kill()
                    
                          
                
                # Asignar puntos según el color del alien
                if alien_type == "blue":
                    if alien.attack_mode:
                        self.score += 100
                    else:
                        self.score += 50
                    alien.kill()
                    
                    
                elif alien_type == "red":
                    if alien.attack_mode:
                        self.score += 160
                    else:
                        self.score += 80
                    alien.kill()  
                
                explosion_position = alien.rect.center
                self.explosion_sprite = Explosion(self.SPRITE_SHEET, self.sprite_explotion_coord, self.explosion_size)
                self.explosion_sprite.start_explosion(explosion_position)
                self.explosion_group.add(self.explosion_sprite)
                
            # Eliminar el láser después de cada colisión 
                laser_sprite.kill()
                
        
        for alien_sprite in self.formation.aliens:
                                
            if pygame.sprite.spritecollide(self.player_sprite, alien_sprite.laser_group, True, pygame.sprite.collide_mask):
                # Reducir una vida
                self.player_sprite.lives -= 1
                # Verificar si el jugador ha perdido todas las vidas
                # if self.player_sprite.lives <= 0:
                #     self.game_over()
                    
                    
            if pygame.sprite.spritecollide(self.player_sprite, self.formation.aliens, True, pygame.sprite.collide_mask):
                # Reducir una vida
                self.player_sprite.lives -= 1
                # Verificar si el jugador ha perdido todas las vidas
                # if self.player_sprite.lives <= 0:
                #     self.game_over() 
        
        
        if len(self.formation.aliens) == 0:
            self.game_over()     
    
    def load_high_score(self):
        """Carga el high score desde un archivo, si el archivo no existe lo inicializa a 0."""
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                try:
                    return int(file.read())
                except:
                    return 0  # Si el archivo está vacío o tiene un valor no válido, retornar 0
        return 0  # Si no existe el archivo, inicializar el high score a 0

    def save_high_score(self):
        """Guarda el high score actual en un archivo."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def check_high_score(self):
        """Verifica si el puntaje actual es mayor que el high score."""
        if self.score > self.high_score:
            self.high_score = self.score
    
    
    
    def draw_Game_Over(self):
        
        game_over_text = self.FONT_score.render("Game Over", True, self.settings.RED)
        
        centered_text_whidt = game_over_text.get_width()
        centered_text = (self.settings.WIDTH/2) - (centered_text_whidt // 2)
        self.SCREEN.blit(game_over_text, (centered_text, 545))
        pygame.display.update()
        
    def draw_score(self):
    # Dibuja el puntaje actual en la pantalla.
        score_text = self.FONT_score.render("1UP", True, self.settings.RED)
        score_text_2 = self.FONT_score.render(f"{self.score}", True, self.settings.WHITE)
        high_score_text_3 = self.FONT_score.render("HIGH SCORE", True, self.settings.RED)
        high_score_text = self.FONT_score.render(f"{self.high_score}", True, self.settings.WHITE)
        
        # Posición fija para "HIGH SCORE"
        score_text_3_x = 250

        # Calcular la posición centrada para high_score_text en relación a "HIGH SCORE"
        score_text_3_width = high_score_text_3.get_width()  # Ancho del texto "HIGH SCORE"
        high_score_text_width = high_score_text.get_width()  # Ancho del high score
        
        # Centrar high_score_text respecto a high_score_text_3
        centered_high_score_x = score_text_3_x + (score_text_3_width // 2) - (high_score_text_width // 2)
        
        # Calcular la posición centrada para score_text_2 respecto a "1UP"
        score_text_width = score_text.get_width()  # Ancho del texto "1UP"
        score_text_2_width = score_text_2.get_width()  # Ancho del puntaje actual
        centered_score_x = 50 + (score_text_width // 2) - (score_text_2_width // 2)

        # Dibujar el texto en pantalla
        self.SCREEN.blit(high_score_text_3, (score_text_3_x, 15))
        self.SCREEN.blit(high_score_text, (centered_high_score_x, 45))
        self.SCREEN.blit(score_text, (30, 15))
        self.SCREEN.blit(score_text_2, (centered_score_x, 45))
   

    def debug(self, info, y=480, x=60, font_size=50, color="white", bg_color=None):
        # Obtener la superficie de la pantalla.
        screen = pygame.display.get_surface()
        
        # Crear una fuente para el texto de depuración.
        font = pygame.font.Font(None, font_size)  # Fuente con el tamaño especificado.
        
        # Renderizar la información de depuración como una superficie de texto.
        debug_surf = font.render(str(info), True, color)
        debug_rect = debug_surf.get_rect(topleft = (x, y))

        # Si se especifica un color de fondo, dibujar el rectángulo de fondo.
        if bg_color:
            pygame.draw.rect(screen, bg_color, debug_rect)

        # Dibujar el texto de depuración en la pantalla.
        screen.blit(debug_surf, debug_rect)
    
    
    def game_over(self):
        self.draw_Game_Over()
        #self.running = False  # Detener el bucle principal
        # Puedes agregar más lógica, como mostrar una pantalla de Game Over
    
    
    def calculate_delta_time(self):
        """Calcula y devuelve el delta_time usando time.time()"""
        # Inicializa `self.last_time` la primera vez que se llama a la función
        if not hasattr(self, "last_time"):
            self.last_time = time.time()
        
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time  # Actualiza `last_time` para el próximo ciclo
        return delta_time

    def run(self):
        self.running = True

        while self.running:
            # Calcular delta_time
            delta_time = self.calculate_delta_time()
            fps = self.clock.get_fps()
            self.clock.tick()  
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    self.running = False

            # Actualizar lógica de la formación
                  
            self.formation.update (delta_time)
            self.background.update(delta_time)
            self.player_group.update(delta_time)
            self.check_for_collision()
            self.check_high_score()  # Verificar si el score actual supera el high score
            for alien_sprite in self.formation.aliens:
                alien_sprite.laser_group.update(delta_time)
            Alien.sprite_animation(delta_time)
            
            # Dibujar
            self.SCREEN.fill(self.settings.BLACK)
            self.background.draw()
            self.formation.draw(self.SCREEN)
            self.player_group.draw(self.SCREEN)
            self.player_sprite.laser_group.draw(self.SCREEN)
            self.draw_score()
            self.player_sprite.draw()
            # Actualizar y dibujar explosiones
            self.explosion_group.update(delta_time)
            self.explosion_group.draw(self.SCREEN)
            
            for alien_sprite in self.formation.aliens:
                alien_sprite.laser_group.draw(self.SCREEN)
               
            if self.player_sprite.lives == 0:
                self.draw_Game_Over()  # Llama a la función para mostrar el texto "Game Over"
                pygame.display.update()
           
           
            fps_text = self.font.render(f"FPS: {int(fps)}", True, (255, 255, 255))  # Blanco
            self.SCREEN.blit(fps_text, (10, 100))  # Posición en la esquina superior izquierda

            
            # Actualizar la pantalla
            
            pygame.display.flip()

        # Salir de Pygame
        pygame.quit()
        sys.exit()




# Clase Alien
class Alien(pygame.sprite.Sprite):
    # Variables de clase para la animación
    animation_frames = []
    global_animation_timer = 0.0
    global_animation_interval = 0.4  # Intervalo entre frames en segundos
    global_animation_index = 0

    # Variables de clase para los sprites
    animation_frames_by_type = {
        "red": [],
        "blue": [],
        "boss_green": [],
        "boss_blue": []
    }

    def __init__(self, mIndex, formation, alien_type, bezier_id, game):
        super().__init__()  # Inicializar la clase base de pygame.sprite.Sprite
        self.game = game
        self.mIndex = mIndex
        self.bezier_id = bezier_id 
        self.formation = formation  # Referencia a la formación
        self.alien_type = alien_type
        self.speed = 1.7  # Velocidad a lo largo de la curva
        self.speed_attack = 2
        self.t = 0.0  # Parámetro para recorrer la curva
        self.curve_index = 0  # Índice de la curva actual
        self.arrived = False  # Indica si el alien ha llegado a su posición objetivo
        self.time_since_start = 0.0  # Tiempo acumulado desde el inicio
        self.active = False  # Indica si el alien está activo
        self.angle = 0.0  # Ángulo de rotación
        self.scale_factor_x = 2.2  # Aumentar al 150% del tamaño original
        self.scale_factor_y = 4.0  # Aumentar al 150% del tamaño original
        
        # Nueva variable para el control de impactos
        self.hit_count = 0  # Lleva la cuenta de los impactos recibidos
        
        # Nuevas variables para controlar el comportamiento en la curva Bézier
        self.curve_start_delay = 0.05 * bezier_id  # Retraso en el inicio de la curva
        self.curve_spacing_factor = 1.0  # Factor de separación en la curva
        self.curve_speed_factor = 1.0  # Factor de velocidad en la curva
        
        # Variables fase ataque
        self.attack_mode = False  # Indica si está en fase de ataque
        self.attack_curves = []  # Puntos de control para la curva de ataque
        self.attack_t = 0.0  # Parámetro para recorrer la curva en fase de ataque
        self.curve_attack_index = 0
        
        # Posición objetivo inicial
        # En la clase Alien, método __init__:

        self.initial_target_x, self.initial_target_y = self.formation.get_initial_target_position(self.mIndex)

        # Desplazamiento del grid
        self.grid_offset_x = 0.0
        
        
        # Atributos para manejar la pausa y la animación de captura
        self.pausing = False
        self.pause_start_time = None
        self.capture_animation_frames = []
        self.capture_animation_frame = None
        

        # Inicializar los frames de animación si aún no se han cargado
        self.load_animation_frames()

        self.animation_frames = Alien.animation_frames_by_type[alien_type]

        # Inicializar la imagen del sprite y el rectángulo
        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.initial_target_x, self.initial_target_y)
        
        # Generar la máscara para el alien
        self.mask = pygame.mask.from_surface(self.image)

        # Variables para el patrón de expansión
        self.expansion_offset = 0.0  # Desplazamiento horizontal durante la expansión
        self.expansion_offset_y = 0.0  # Desplazamiento vertical durante la expansión

        # Definir la posición inicial del alien y las curvas
        self.define_curves_and_position()
        
        self.move_to_final_position = False  # Indicador de movimiento hacia la posición final
        self.final_move_progress = 0.0  # Progreso del movimiento hacia la posición final
        self.start_position = np.array([self.x, self.y])  # Posición inicial para la interpolación
        self.final_target_position = np.array([self.initial_target_x, self.initial_target_y])  # Posición final en el grid
        
         # Variables para el control del final de la curva y el movimiento final
        self.reached_curve_end = False  # Nueva variable para saber si llegó al final de la curva
        self.final_move_progress = 0.0  # Progreso de movimiento hacia el grid

        self.laser_group = pygame.sprite.Group()
        self.shoot_cooldown = 400  # Tiempo de enfriamiento entre disparos
        self.last_shot_time = 0

        self.capture_player = CapturePlayer(self, game) 
        self.curvas_relativas = Curvas_relativas (self, formation, game)
        self.is_capture_formation = False  # Indica si el alienígena está en una formación de captura
        
       
        
        
    # def start_capture(self):
    #     self.capture_player.define_capture_curves_1()  # Llama a la captura específica
    #     self.capture_player.define_capture_curves_2()  # Llama a la captura específica
    def on_laser_hit(self):
        """Maneja lo que sucede cuando el alien es impactado por un láser."""
        if self.alien_type == "boss_green" and self.hit_count == 0:
            # Primer impacto: cambiar de boss_green a boss_blue
            self.alien_type = "boss_blue"
            self.animation_frames = Alien.animation_frames_by_type["boss_blue"]
            self.hit_count += 1
        elif self.alien_type == "boss_blue" and self.hit_count == 1:
            
            if self.formation.attack_mode:
                self.formation.game.score += 400
            else:
                self.formation.game.score += 150
            # Segundo impacto: destruir el alien
            #self.formation.game.score += 150
            self.kill()

    def load_animation_frames(self):
        """Carga los frames de animación de los sprites."""
        if not Alien.animation_frames_by_type[self.alien_type]:  
            if self.alien_type == "red":
                Alien.animation_frames_by_type["red"] = [
                    self.formation.game.get_sprite((109, 73, 16, 16)),
                    self.formation.game.get_sprite((127, 73, 16, 16))
                ]
            elif self.alien_type == "blue":
                Alien.animation_frames_by_type["blue"] = [
                    self.formation.game.get_sprite((109, 91, 16, 16)),
                    self.formation.game.get_sprite((127, 91, 16, 16))
                ]
            elif self.alien_type == "boss_green":
                Alien.animation_frames_by_type["boss_green"] = [
                    self.formation.game.get_sprite((109, 37, 16, 16)),
                    self.formation.game.get_sprite((127, 37, 16, 16))
                ]
                Alien.animation_frames_by_type["boss_blue"] = [
                    self.formation.game.get_sprite((109, 55, 16, 16)),
                    self.formation.game.get_sprite((127, 55, 16, 16))
                ]

        if not self.capture_animation_frames:
            self.capture_animation_frames = [
            self.formation.game.get_sprite((289, 36, 48, 80)),
            self.formation.game.get_sprite((339, 36, 48, 80)),
            self.formation.game.get_sprite((389, 36, 48, 80))
        ]
        
            scaled_frames = []
            for frame in self.capture_animation_frames:
                # Obtener el tamaño original
                original_size = frame.get_size()
                # Calcular el nuevo tamaño usando el factor de escala
                new_size = (int(original_size[0] * self.scale_factor_x), int(original_size[1] * self.scale_factor_y))
                # Escalar el frame
                scaled_frame = pygame.transform.scale(frame, new_size)
                # Agregar el frame escalado a la lista
                scaled_frames.append(scaled_frame)

            # Reemplazar la lista original con los frames escalados
            self.capture_animation_frames = scaled_frames 
            
            for key in Alien.animation_frames_by_type:
                frames = Alien.animation_frames_by_type[key]
                for i in range(len(frames)):
                    frames[i] = frames[i].convert_alpha()
            
    def define_curves_and_position(self):
        """Define las curvas y la posición inicial del alien."""
        # Definir curvas basadas en el tipo de alien
        if self.alien_type == "red":
            self.define_red_curves()
        elif self.alien_type == "blue":
            self.define_blue_curves()
        elif self.alien_type == "boss_green":
            self.define_boss_green_curves()  
        
            self.start_x, self.start_y = self.curves[0][0]
            # self.start_delay = self.bezier_id* 0.2

        # Definir posición inicial
        self.x = self.start_x
        self.y = self.start_y

    def define_red_curves(self):
        """Define las curvas específicas para los alienígenas rojos."""
        if self.mIndex in [0, 1, 2, 3]:
            self.curves = [
                self.control_points(),
                self.control_points_2()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = self.bezier_id * 0.2
        elif self.mIndex in [4, 5, 6, 7]:
            self.curves = [
                self.control_points_3(),
                self.control_points_4(),
                self.control_points_5()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = self.bezier_id * 0.25
        elif self.mIndex in [8, 9, 10, 11, 12, 13, 14, 15]:
            self.curves = [
                self.control_points_6(),
                self.control_points_7(),
                self.control_points_8()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)

    def define_blue_curves(self):
        """Define las curvas específicas para los alienígenas azules."""
        if self.mIndex in [16, 17, 18, 19]:
            self.curves = [
                self.control_points_12(),
                self.control_points_13()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)
        elif self.mIndex in [20, 21, 22, 23, 24, 25, 26, 27]:
            self.curves = [
                self.control_points_14(),
                self.control_points_15()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)
        elif self.mIndex in [28, 29, 30, 31, 32, 33, 34, 35]:
            self.curves = [
                self.control_points_10(),
                self.control_points_11()
            ]
        self.start_x, self.start_y = self.curves[0][0]
        self.start_delay = (self.bezier_id * 0.2)
        
    def define_boss_green_curves(self):
        """Define las curvas específicas para los alienígenas azules."""
        if self.mIndex in [36, 37, 38, 39]:
            self.curves = [
                self.control_points_3(),
                self.control_points_4(),
                self.control_points_5()
            ]
           
        self.start_x, self.start_y = self.curves[0][0]
        self.start_delay = (self.bezier_id * 0.25 + 0.88)

        
        

    def control_points(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [188, -10],
            [320, 230],
            [560, 260],
            [580, 450]
        ])

    def control_points_2(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [580, 450],
            [592, 638],
            [352, 657],
            [342, 463]
        ])
    def control_points_3(self):
        # Puntos de control originales para aliens 4-7
        return np.array([
            ([-5, 706]),
            ([205, 659]),
            ([263, 524]),
            ([212, 463])
        ])

    def control_points_4(self):
        return (
            np.array([212, 463]),
            np.array([163, 356]),
            np.array([15, 410]),
            np.array([56, 517])
        )

    def control_points_5(self):
        # El último punto de control es la posición objetivo actual (sin movimiento lateral)
        return (
            np.array([56, 517]),
            np.array([123, 619]),
            np.array([248, 561]),
            np.array([260, 463])
        )

    def control_points_6(self):
        width = self.formation.game.settings.WIDTH
        return (
            np.array([width + 5, 706]),
            np.array([width - 205, 659]),
            np.array([width - 263, 524]),
            np.array([width - 212, 463])
        )

    def control_points_7(self):
        width = self.formation.game.settings.WIDTH
        return (
            np.array([width - 212, 463]),
            np.array([width - 163, 356]),
            np.array([width - 15, 410]),
            np.array([width - 56, 517])
        )

    def control_points_8(self):
        width = self.formation.game.settings.WIDTH
        return (
            np.array([width - 56, 517]),
            np.array([width - 123, 619]),
            np.array([width - 248, 561]),
            np.array([width - 260, 463])
        )

    def control_points_9(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [170, -10],
            [268, 250],
            [560, 195],
            [600, 385]
        ])
    def control_points_10(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [250, -10],
            [320, 250],
            [560, 195],
            [580, 385]
        ])
    

    def control_points_11(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [580, 385],
            [590, 650],
            [280, 680],
            [330, 415]
        ]) 
    def control_points_12(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [width - 188, -10],
            [width - 320, 230],
            [width - 560, 260],
            [width - 580, 450]
        ])
    def control_points_13(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [width - 580, 450],
            [width - 592, 638],
            [width - 352, 657],
            [width - 342, 463]

        ])
        
    def control_points_14(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [width - 250, -10],
            [width - 320, 250],
            [width - 560, 195],
            [width - 580, 385]

        ])   
        
        
    def control_points_15(self):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [width - 580, 385],
            [width - 650, 650],
            [width - 280, 680],
            [width - 300, 415]

        ])      
        
  
    def bezier_curve(self, points, t):
        """Calcula el punto en la curva Bézier cúbica para un valor de t dado."""
        return (
            (1 - t) ** 3 * points[0] +
            3 * (1 - t) ** 2 * t * points[1] +
            3 * (1 - t) * t ** 2 * points[2] +
            t ** 3 * points[3]
        )



    def bezier_derivative(self, points, t):
        """Calcula la derivada en la curva Bézier cúbica para un valor de t dado."""
        derivative = (
            3 * (1 - t) ** 2 * (points[1] - points[0]) +
            6 * (1 - t) * t * (points[2] - points[1]) +
            3 * t ** 2 * (points[3] - points[2])
        )
        return derivative

    def is_left_alien(self):
        """Determina si el alien pertenece a la mitad izquierda del grid."""
        return self.mIndex % 2 == 0

    def is_top_row(self):
        """Determina si el alien pertenece a la fila superior."""
        pos_in_group = self.mIndex % 4
        return pos_in_group == 0 or pos_in_group == 1


    @classmethod
    def sprite_animation(cls, delta_time):
        cls.global_animation_timer += delta_time
        if cls.global_animation_timer >= cls.global_animation_interval:
            cls.global_animation_timer -= cls.global_animation_interval

            # Ajustar global_animation_index para no exceder el tamaño de los frames de animación
            # Suponemos que todos los tipos tienen la misma cantidad de frames
            max_index = len(cls.animation_frames_by_type["red"])
            cls.global_animation_index = (cls.global_animation_index + 1) % max_index



    def define_attack_curves_1_1(self, offset_x=0):
        if self.alien_type == "red" or "blue":
            self.attack_curves = [
                self.attack_control_points_1_1(offset_x),
                self.attack_control_points_1_2(offset_x),
                self.attack_control_points_1_3(offset_x),
                self.attack_control_points_1_4(offset_x)
            ]
            
    def define_attack_curves_2_1(self, offset_x=0):
        if self.alien_type == "red"or "blue":
            self.attack_curves = [
                self.attack_control_points_2_1(offset_x),
                self.attack_control_points_2_2(offset_x),
                self.attack_control_points_2_3(offset_x),
                self.attack_control_points_2_4(offset_x)
            ]

    def define_attack_curves(self, offset_x=0):
        if self.alien_type == "blue":
            self.attack_curves = [
                self.attack_control_points_1_1(offset_x),
                self.attack_control_points_1_2(offset_x),
                self.attack_control_points_1_3(offset_x),
                self.attack_control_points_1_4(offset_x)
            ]

    def define_attack_curves_2(self, offset_x=0 ) : 
        random_xx =  random.randint(-50, 120)
        if self.alien_type == "blue":
            self.attack_curves = [
                self.attack_control_points_4(random_xx, offset_x),
                self.attack_control_points_5(random_xx, offset_x),
                self.attack_control_points_6(random_xx, offset_x)
                
            ]

    def define_attack_curves_3(self, offset_x=0):
        random_xx =  random.randint(-150, 50)
        if self.alien_type == "blue":
            self.attack_curves = [
                self.attack_control_points_8(random_xx, offset_x),
                self.attack_control_points_9(random_xx, offset_x),
                self.attack_control_points_10(random_xx, offset_x)
            
        ]

        
    def define_attack_curves_4(self, offset_x=0):
        self.attack_curves = [
            
            self.attack_control_points_11(offset_x),
            self.attack_control_points_12(offset_x)
        ]       


    def attack_control_points_1_1(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [self.x, self.y],  # Comienza desde la posición actual
            [174, 96],  # Un ejemplo de punto intermedio
            [50, 250],  # Otro punto
            [300, 395]  # Final en una posición aleatoria
        ])
        
    def attack_control_points_1_2(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [300, 395] ,  # Comienza desde la posición actual
            [480, 455],  # Un ejemplo de punto intermedio
            [470, 620],  # Otro punto
            [370, 650]  # Final en una posición aleatoria
        ])
        
    def attack_control_points_1_3(self, offset_x=0):
        player_x = self.formation.game.player_sprite.rect.centerx  # Obtener la posición en X del jugador
        return np.array([
            [370, 650],     # Comienza desde la posición actual
            [130, 775],     # Punto intermedio
            [495, 815],     # Otro punto
            [player_x, 1000]  # Final en la posición X del jugador
        ])   
            
    def attack_control_points_1_4(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(350, 600)
        return np.array([
            [240, -10] ,  # Comienza desde la posición actual
            [150, 55],  # Un ejemplo de punto intermedio
            [270, 85],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ]) 
    def attack_control_points_2_1(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [self.x, self.y],  # Comienza desde la posición actual
            [width - 174, 96],  # Un ejemplo de punto intermedio
            [width - 50, 250],  # Otro punto
            [width - 300, 395]  # Final en una posición aleatoria
        ])
        
    def attack_control_points_2_2(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [width - 300, 395] ,  # Comienza desde la posición actual
            [width - 480, 455],  # Un ejemplo de punto intermedio
            [width - 470, 620],  # Otro punto
            [width - 370, 650]  # Final en una posición aleatoria
        ])
        
    def attack_control_points_2_3(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        player_x = self.formation.game.player_sprite.rect.centerx  # Obtener la posición en X del jugador
        return np.array([
            [width - 370, 650],     # Comienza desde la posición actual
            [width - 130, 775],     # Punto intermedio
            [width - 495, 815],     # Otro punto
            [player_x, 1000]  # Final en la posición X del jugador
        ])   
            
    def attack_control_points_2_4(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(350, 600)
        return np.array([
            [width - 240, -10] ,  # Comienza desde la posición actual
            [width - 150, 55],  # Un ejemplo de punto intermedio
            [width - 270, 85],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ]) 

    def pause_and_capture_animation(self, delta_time):
        if self.performing_capture:
            if self.capture_start_time is None:
                # Iniciar el tiempo de captura
                self.capture_start_time = pygame.time.get_ticks()

            elapsed_time = (pygame.time.get_ticks() - self.capture_start_time) / 1000.0
            if elapsed_time < 5:
                # Reproducir la animación "capture_player"
                frame_index = int((elapsed_time * 1000) // 500) % 10  # Cambiar de frame cada 500 ms
                if frame_index == 0:
                    sprite = self.formation.game.get_sprite((289, 36, 48, 80))
                elif frame_index == 1:
                    sprite = self.formation.game.get_sprite((339, 36, 48, 80))
                else:
                    sprite = self.formation.game.get_sprite((389, 36, 48, 80))

                # Obtener la posición en el borde inferior central del alien boss_green
                sprite_rect = sprite.get_rect(midbottom=(self.x, self.y))

                # Dibujar el sprite en la pantalla
                self.formation.game.SCREEN.blit(sprite, sprite_rect)
            else:
                # Finalizar la captura y continuar con la siguiente curva
                self.performing_capture = False
                self.capture_start_time = None

        pygame.display.flip()  # Actualizar la pantalla



    def attack_control_points_2(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        player_x = self.formation.game.player_sprite.rect.centerx  # Obtener la posición en X del jugador
        return np.array([
            [200, 660],  # Comienza desde la posición actual
            [300, 760],  # Un ejemplo de punto intermedio
            [330, 780],  # Otro punto
            [player_x, 1000]  # Final en una posición aleatoria
        ])

    def attack_control_points_3(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(120, 130)
        return np.array([
            
            [120, -10],
            #[random_x, -10],  # Comienza desde la posición actual
            [110, 115],  # Un ejemplo de punto intermedio
            [365, 80],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ])

    def attack_control_points_4(self, random_xx, offset_x=0) :
        return np.array([
            
            [self.x, self.y],  # Comienza desde la posición actual
            [110 + random_xx, 270],  # Punto intermedio ajustado
            [10 + random_xx, 340],  # Otro punto ajustado
            [170 + random_xx, 430]   # Final ajustado
        ])

    def attack_control_points_5(self, random_xx, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(150, 160)
        return np.array([
            
            [170 + random_xx, 430], 
            [470 + random_xx, 605],
            [435 + random_xx, 920],
            [325 + random_xx, 925]
    ])

    def attack_control_points_6(self, random_xx, offset_x=0):
        width = self.formation.game.settings.WIDTH
        player_x = self.formation.game.player_sprite.rect.centerx  # Obtener la posición en X del jugador
        return np.array([
            
            [325 + random_xx, 925],
            [195 + random_xx, 920],  # Un ejemplo de punto intermedio
            [150 + random_xx, 895],  # Otro punto
            [self.x, self.y] # Final en una posición aleatoria
        ])
        
    def attack_control_points_7(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(350, 600)
        return np.array([
            
            [135, 340],
            [150, 895],  # Un ejemplo de punto intermedio
            [195, 920],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ])       

    def attack_control_points_8(self, random_xx, offset_x=0):
        width = self.formation.game.settings.WIDTH
        return np.array([
            [self.x, self.y],  # Comienza desde la posición actual
            [width - 110 + random_xx, 270],  # Punto intermedio ajustado
            [width - 10 + random_xx, 340],  # Otro punto ajustado
            [width - 170 + random_xx, 430]   # Final en una posición aleatoria
        ])

    def attack_control_points_9(self, random_xx, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(155, 165)
        return np.array([
            [width - 170 + random_xx, 430], 
            [width - 470 + random_xx, 605],
            [width - 435 + random_xx, 920],
            [width - 325 + random_xx, 925]
        ])

    def attack_control_points_10(self, random_xx, offset_x=0):
        width = self.formation.game.settings.WIDTH
        
        return np.array([
            [width - 325 + random_xx, 925],
            [width - 195 + random_xx, 920],  # Un ejemplo de punto intermedio
            [width - 150 + random_xx, 895],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ])    
        
    def attack_control_points_11(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(350, 600)
        return np.array([
            
            [width - 170, -10],
            [width - 190, 100],  # Un ejemplo de punto intermedio
            [width - 265, 55],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ])   
        
        
    def attack_control_points_12(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(160, 170)
        return np.array([
            [265, 660],  # Comienza desde la posición actual
            [315, 760],  # Un ejemplo de punto intermedio
            [285, 850],  # Otro punto
            [random_x, 1000]  # Final en una posición aleatoria
        ])

    def attack_control_points_13(self, offset_x=0):
        width = self.formation.game.settings.WIDTH
        random_x = random.randint(140, 150)
        return np.array([
            [random_x, -10],  # Comienza desde la posición actual
            [135, 40],  # Un ejemplo de punto intermedio
            [315, 50],  # Otro punto
            [self.x, self.y]  # Final en una posición aleatoria
        ])          
        
        
    
    def shoot(self, delta_time):
        current_time = pygame.time.get_ticks()
        if self.attack_mode and self.curve_attack_index <=  1: 
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.last_shot_time = current_time
                if random.random() < 0.1:  # Probabilidad de disparo
                    # Pasar la posición del jugador al láser
                    player_position = self.formation.game.player_sprite.rect.center
                    
                    # Decidir si disparo es preciso o con variación
                    if random.random() < 0.5:  # 50% de disparos precisos
                        laser = AlienLaser(self.rect.center, player_position, self.game, error_margin=0)
                    else:  # 50% de disparos con variación
                        laser = AlienLaser(self.rect.center, player_position, self.game, error_margin=75)
                    
                    self.laser_group.add(laser)       
                    
                    
    def reset_attack_state(self):
        self.attack_t = 0.0
        self.curve_attack_index = 0
        self.reached_curve_end = False
        self.pausing = False
        self.pause_start_time = None
        self.is_capture_formation = False
        self.returning_to_grid = False
        self.final_move_progress = 0.0
     
        # Restablecer cualquier otra variable relacionada con el ataque
    
    
    def debug_2(self, surface):
        if self.alien_type == 'boss_green' or self.alien_type == 'boss_blue':
            # Crear una lista con los nombres y valores de las variables
            debug_info = [
                #f"attack_t: {self.attack_t:.2f}",
                f"tipo curva: {self.define_attack_curves}",
                f"curve_attack_idx: {self.mIndex}",
                f"curve_attack_idx: {self.curve_attack_index}",
                f"reached_end: {self.reached_curve_end}",
                f"pausing: {self.pausing}",
                f"pause_start: {self.pause_start_time}",
                f"is_capture: {self.is_capture_formation}"
            ]

            font = self.formation.game.FONT

            # Posición inicial para dibujar el texto (ajusta según necesites)
            text_x = int(self.x) - 250 + (self.mIndex % 4) * 80 
            # Desplazamiento en Y basado en el mIndex para evitar superposición
            text_y = int(self.y) + 250 + (self.mIndex % 4) * 150  # Ajusta el multiplicador según sea necesario

            # Color del texto
            text_color = (255, 255, 255)  # Blanco

            # Renderizar y dibujar cada línea de información
            for i, line in enumerate(debug_info):
                text_surface = font.render(line, True, text_color)
                surface.blit(text_surface, (text_x, text_y + i * 25))

    def get_rotated_image(self, angle):
        # Redondear el ángulo para limitar el número de rotaciones únicas
        rounded_angle = int(angle) % 360  # Asegura que el ángulo esté entre 0 y 359
        key = (self.alien_type, rounded_angle)
        if key in self.rotated_images_cache:
            return self.rotated_images_cache[key]
        else:
            # Rotar y almacenar en caché
            rotated_image = pygame.transform.rotate(self.image, -rounded_angle)
            self.rotated_images_cache[key] = rotated_image
            return rotated_image    
                

    def update(self, delta_time):
        
        # Actualizar la imagen del alien si ha cambiado el tipo
        if self.alien_type == "boss_blue" and self.hit_count == 1:
            self.image = self.animation_frames[0]
        
        self.time_since_start += delta_time
    
        # Verificar si el alien puede activarse según la fase actual de la formación
        if not self.active:
            current_phase = self.formation.current_phase

            if current_phase == 0 and self.mIndex in [0, 1, 2, 3, 16, 17, 18, 19]:
                if self.time_since_start >= self.start_delay:
                    self.active = True
                                    

            elif current_phase == 2 and self.mIndex in [4, 5, 6, 7, 36, 37, 38, 39]:
                                        
                if self.time_since_start >= self.start_delay - 0.5:
                    self.active = True
                    

            elif current_phase == 3 and self.mIndex in range(8, 16):
                if self.time_since_start >= self.start_delay - 1:
                    self.active = True

            elif current_phase == 4 and self.mIndex in range(20, 28):
                if self.time_since_start >= self.start_delay:
                    self.active = True

            elif current_phase == 5 and self.mIndex in range(28, 36):
                if self.time_since_start >= self.start_delay - 2:
                    self.active = True
        
        if self.attack_mode:
            
            if self.pausing:
                # Manejar la pausa y la animación
                current_time = pygame.time.get_ticks()
                if self.pause_start_time is None:
                    self.pause_start_time = current_time
                elapsed_time = (current_time - self.pause_start_time) / 1000.0

                if elapsed_time >= 4.0:
                    self.pausing = False
                    self.pause_start_time = None
                    self.curve_attack_index += 1
                    self.attack_t = 0.0
                else:
                    # Mantener la posición y actualizar la animación
                    # No actualizar self.x y self.y
                    animation_duration = 4.0
                    num_frames = len(self.capture_animation_frames)
                    frame_duration = (animation_duration / num_frames)/10
                    frame_index = int((elapsed_time % animation_duration) / frame_duration) % num_frames
                    self.capture_animation_frame = self.capture_animation_frames[frame_index]
                    # No continuar con el movimiento durante la pausa
                    return
            else:
            # Movimiento normal de ataque
                self.attack_t += self.speed_attack * delta_time * 0.4
                if self.attack_t > 1.0:
                    self.attack_t = 1.0

                if self.curve_attack_index < len(self.attack_curves):
                    attack_points = self.attack_curves[self.curve_attack_index]
                    position = self.bezier_curve(attack_points, self.attack_t)
                    self.x, self.y = position

                    derivative = self.bezier_derivative(attack_points, self.attack_t)
                    dx, dy = derivative
                    angle = np.degrees(np.arctan2(dy, dx))
                    self.angle = angle + 90
                    
                    if self.curve_attack_index == 1 and self.alien_type == 'boss_green' and self.is_capture_formation or self.alien_type == "boss_blue" and self.is_capture_formation:
                        # Aquí puedes modificar el ángulo según necesites
                        # Por ejemplo, agregar un ángulo fijo
                        self.angle = 180
                    else:
                        self.angle = angle + 90
                    

                    if self.attack_t >= 1.0:
                        # Verificar si necesitamos pausar
                        if self.curve_attack_index == 0 and self.alien_type == "boss_green" and self.is_capture_formation:
                            self.pausing = True
                            self.pause_start_time = None
                            # Mantener la posición al final de la primera curva
                            self.x, self.y = self.bezier_curve(attack_points, 1.0)
                            self.angle = 0.0 +  180
                        else:
                            self.attack_t = 0.0
                            self.curve_attack_index += 1
                else:
                    # Preparar retorno al grid
                    self.attack_mode = False
                    self.returning_to_grid = True
                    self.start_x, self.start_y = self.x, self.y
                    self.final_move_progress = 0.0
                    
        elif getattr(self, 'returning_to_grid', False):
            # Movimiento de retorno al grid
            self.final_move_progress += self.speed * delta_time
            
            if self.final_move_progress >= 1.0:
                self.final_move_progress = 1.0
                self.returning_to_grid = False
                self.arrived = True
                self.angle = 0.0
                
                

            self.x = (1 - self.final_move_progress) * self.start_x + self.final_move_progress * (self.initial_target_x + self.grid_offset_x)
            self.y = (1 - self.final_move_progress) * self.start_y + self.final_move_progress * self.initial_target_y

            dx = (self.initial_target_x + self.grid_offset_x) - self.start_x
            dy = self.initial_target_y - self.start_y
            angle = np.degrees(np.arctan2(dy, dx))
            self.angle = angle + 90
            self.reset_attack_state()            
                    
                    
        elif self.active and not self.arrived:
            # Moverse a lo largo de la curva Bézier
            if not self.reached_curve_end:
                self.t += (self.speed * self.curve_speed_factor * delta_time * self.curve_spacing_factor)
                if self.t > 1.0:
                    self.t = 1.0
                points = self.curves[self.curve_index]
                points = np.array(points)

                position = self.bezier_curve(points, self.t)
                derivative = self.bezier_derivative(points, self.t)
                self.x, self.y = position
                
                dx, dy = derivative
                angle = np.degrees(np.arctan2(dy, dx))
                self.angle = angle + 90

                if self.t >= 1.0:
                    self.t = 0.0
                    self.curve_index += 1
                    if self.curve_index >= len(self.curves):
                        self.reached_curve_end = True
                        self.final_move_progress = 0.0
                        self.start_x, self.start_y = self.x, self.y

            # Movimiento suave hacia la posición final en el grid
            if self.reached_curve_end and not self.arrived:
                self.final_move_progress += self.speed * delta_time
                if self.final_move_progress >= 1.0:
                    self.final_move_progress = 1.0

                self.x = (1 - self.final_move_progress) * self.start_x + self.final_move_progress * (self.initial_target_x + self.grid_offset_x)
                self.y = (1 - self.final_move_progress) * self.start_y + self.final_move_progress * self.initial_target_y

                dx = (self.initial_target_x + self.grid_offset_x) - self.start_x
                dy = self.initial_target_y - self.start_y
                angle = np.degrees(np.arctan2(dy, dx))
                self.angle = angle + 90

                if self.final_move_progress >= 1.0:
                    self.arrived = True
                    self.angle = 0.0           
                    
                                
                    
                    

        elif self.arrived:
            # **Aplicar el desplazamiento de expansión aquí**
            self.x = self.initial_target_x + self.grid_offset_x + self.expansion_offset
            self.y = self.initial_target_y + self.expansion_offset_y
            self.angle = 0.0  # Sin rotación al llegar
            #self.attack_mode = True

        # Actualizar el frame de animación
        rotated_image = pygame.transform.rotate(self.animation_frames[Alien.global_animation_index], -self.angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        # Actualizar la máscara para la colisión
        self.mask = pygame.mask.from_surface(self.image)

        # Actualizar la animación global
        # Alien.sprite_animation(delta_time)
        # if 0 <= Alien.global_animation_index < len(self.animation_frames):
        #     self.image = self.animation_frames[Alien.global_animation_index]

        # **Fase de ataque**
        
                   
    
            
        # Actualizar rect y máscara
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.mask = pygame.mask.from_surface(self.image)

        # Actualizar la animación global
        
        self.shoot(delta_time)                
                
    def draw_bezier_path(self, surface):
    # Número de puntos para la línea de puntos
        num_points = 50
        curve_colors = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0)]  # Colores para cada curva
        control_colors = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (0, 255, 0)]  # Colores para los puntos de control
        radius = 3  # Tamaño de los puntos de control

        
        if self.attack_mode:
            # Número de puntos para la línea de puntos
            num_points = 50  # Aumenta o disminuye el número de puntos para ajustar la calidad del dibujo
            curve_color = (255, 255, 255)  # Color de la curva
            radius = 2  # Tamaño de los puntos de control (opcional)

            # Asegurarse de que haya curvas de ataque definidas
            if len(self.attack_curves) > 0:
                for curve_index, curve in enumerate(self.attack_curves):
                    previous_point = None  # Almacena el punto anterior para dibujar líneas entre puntos

                    # Dibujar la línea punteada de la curva
                    for i in range(num_points + 1):
                        t = i / num_points  # Valor de t entre 0 y 1
                        point = self.bezier_curve(curve, t)  # Calcular el punto en la curva
                        x, y = int(point[0]), int(point[1])  # Convertir las coordenadas a enteros

                        # Dibujar un pequeño círculo en cada punto de la curva (para hacerla punteada)
                        if previous_point:
                            if i % 2 == 0:  # Hacer líneas punteadas (dibujar en cada 2do punto)
                                pygame.draw.line(surface, curve_color, previous_point, (x, y), 1)

                        previous_point = (x, y)  # Actualizar el punto anterior para la siguiente línea

                    # Opcional: dibujar los puntos de control
                    for control_point in curve:
                        control_x, control_y = int(control_point[0]), int(control_point[1])

                        # Dibujar un círculo para el punto de control (opcional)
                        pygame.draw.circle(surface, curve_color, (control_x, control_y), radius)

            
        
        
        if len(self.curves) > 0:
            for curve_index, curve in enumerate(self.curves):
                # Escoger el color de la curva y de los puntos de control
                curve_color = curve_colors[curve_index % len(curve_colors)]
                control_color = control_colors[curve_index % len(control_colors)]

                # Dibujar la línea punteada de la curva
                for i in range(num_points + 1):
                    t = i / num_points  # Valor de t entre 0 y 1
                    point = self.bezier_curve(curve, t)  # Calcular el punto en la curva
                    x, y = int(point[0]), int(point[1])  # Convertir las coordenadas a enteros

                    # Dibujar un círculo en cada punto de la curva
                    #pygame.draw.circle(surface, curve_color, (x, y), radius - 1)

                # Dibujar los puntos de control con sus coordenadas
                for control_point in curve:
                    control_x, control_y = int(control_point[0]), int(control_point[1])

                    # Dibujar un círculo para el punto de control
                    #pygame.draw.circle(surface, control_color, (control_x, control_y), radius + 2)

                    # Dibujar el valor (x, y) del punto de control sobre el punto
                    text_surface = self.formation.game.FONT.render(f"({control_x}, {control_y})", True, control_color)
                    # surface.blit(text_surface, (control_x + 5, control_y + 5))  # Colocar el texto cerca del punto de control


    

    def draw(self, surface):
        if self.active or self.arrived or self.attack_mode or self.pausing:
            
            # Obtener el frame de animación actual
            
            frames = self.animation_frames_by_type[self.alien_type]
            self.image = frames[self.global_animation_index]
            
            
            
            # Rotar la imagen
            self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
            rect = self.rotated_image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.rotated_image, rect)
            
            if self.pausing and self.capture_animation_frame:
                # Dibujar la animación de captura en la parte inferior central del alienígena
                animation_frame = self.capture_animation_frame
                frame_rect = animation_frame.get_rect(midtop=rect.midbottom)
                
                surface.blit(animation_frame, frame_rect)
            
            #Renderizar el texto del mIndex
            text = self.formation.game.FONT.render(str(self.mIndex), True, self.game.settings.WHITE)
            text_rect = text.get_rect(center=(int(self.x), int(self.y) ))
            #surface.blit(text, text_rect)
            
        #self.draw_bezier_path(surface)
        #self.debug_2(surface)
# Clase Formation
class Formation:
    def __init__(self, game):
        self.game = game
          
        self.aliens = pygame.sprite.Group()  # Grupo de sprites para los alienígenas
        self.grid_size_x = 20.0
        self.grid_size_y = 35.0

        # Movimiento lateral del grid durante la llegada de los aliens
        self.move_distance = 40  # Distancia total de movimiento lateral del grid
        self.move_speed = 50  # Velocidad de movimiento lateral del grid (píxeles por segundo)
        self.direction = 1  # 1: derecha, -1: izquierda
        self.current_move = 0  # Movimiento lateral acumulado del grid
        self.lateral_movement_active = True  # El movimiento lateral está activo

        # Movimiento lateral después de que los aliens hayan llegado
        self.aliens_arrived = False  # Indica si todos los aliens han llegado

        self.initial_target_positions = []  # Posiciones objetivo iniciales (sin movimiento)
        self.create_formation()

        # Variables para el patrón de expansión continuo
        self.expanding = False
        self.expansion_duration = 2.0  # Duración total de cada ciclo de expansión
        self.expansion_elapsed = 0.0

        # Fases de llegada de alienígenas
        self.current_phase = 0  # Índice de la fase actual

        # Temporizadores para ataques
        self.attack_mode = False
        self.attack_timer = 0.0
        self.attack_interval = random.uniform(1.0, 2.0)
        self.attack_formations = []
        self.define_attack_formations()
        self.allowed_attack_types = ['red', 'blue', 'boss_green', 'boss_green, red, red']
        #self.curvas_relativas = Curvas_relativas (self)
    def create_formation(self):
        """Crear alienígenas y calcular sus posiciones objetivo."""
        self.add_aliens_to_group("red", 16)
        self.add_aliens_to_group("blue", 20, offset=16)
        self.add_aliens_to_group("boss_green", 4, offset=36)

    def add_aliens_to_group(self, alien_type, count, offset=0):
        """Agrega un grupo de alienígenas a la formación."""
        for mIndex in range(count):
            bezier_id = mIndex
            x, y = self.calculate_target_position(mIndex, alien_type)
            self.initial_target_positions.append((x, y))
            alien = Alien(mIndex + offset, self, alien_type, bezier_id, self.game)
            self.aliens.add(alien)

    def calculate_target_position(self, mIndex, alien_type):
        
        if alien_type == "boss_green":
            # Posicionar los 4 alienígenas verdes en una sola fila con simetría alrededor del centro
            row = 2  # Fila específica para los alienígenas verdes (tercera fila, indexada como 2)
            
            # Alternar la posición en X para cada alien en el grupo de 4
            if mIndex == 0 or mIndex == 2:
                # Lado izquierdo
                sign = -1
            else:
                # Lado derecho
                sign = 1

            # Asignar el desplazamiento horizontal basado en el índice
            col = mIndex // 2  # 0 o 1 para cada par de alienígenas en el lado izquierdo y derecho
            retVal_x = (self.grid_size_x + self.grid_size_x * 2 * col) * sign

            # Asignar la posición en Y para la única fila de alienígenas verdes
            retVal_y = (row * self.grid_size_y) + 70
        
        else:
            group = mIndex // 4
            pos_in_group = mIndex % 4

            # Posición en Y
            if pos_in_group == 0 or pos_in_group == 1:
                retVal_y = self.grid_size_y * 0  # Primera fila
            else:
                retVal_y = self.grid_size_y * 1  # Segunda fila

            # Alternar posición en X para cada alien en el grupo
            if pos_in_group == 0 or pos_in_group == 2:
                # Lado izquierdo
                sign = -1
            else:
                # Lado derecho
                sign = 1

            retVal_x = (self.grid_size_x + self.grid_size_x * 2 * group) * sign

            # Ajustar posiciones para la pantalla
            screen_x = retVal_x + self.game.settings.WIDTH // 2
            screen_y = retVal_y + 180  # Posición objetivo en Y
            
            if alien_type == "blue":
                screen_y += 70
            # elif alien_type == "boss_green":
            #     screen_y += 350
            return int(screen_x), int(screen_y)
        
        # Ajustar posiciones para la pantalla para los alienígenas verdes
        screen_x = retVal_x + self.game.settings.WIDTH // 2
        screen_y = retVal_y  # Posición objetivo en Y para los alienígenas verdes

        return int(screen_x), int(screen_y)

    def get_initial_target_position(self, mIndex):
        return self.initial_target_positions[mIndex]

    def get_grid_center(self):
        """Calcula el centro del grid."""
        xs, ys = zip(*self.initial_target_positions)
        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)
        return center_x, center_y

    def get_adjusted_index(self, alien):
        if alien.alien_type == "red":
            group = alien.mIndex // 4
        elif alien.alien_type == "blue":
            group = (alien.mIndex - 16) // 4  # Ajuste para los alienígenas azules
        elif alien.alien_type == "boss_green":
            group = (alien.mIndex - 36) // 4
        else:
            group = 0  # Valor por defecto para otros tipos de alienígenas              
            
        adjusted_index = group
        return adjusted_index
    
    def all_aliens_in_final_position(self):
        """Verifica si todos los alienígenas han alcanzado su posición final en el grid."""
        return all(alien.arrived for alien in self.aliens)
                

    def apply_expansion(self, delta_time):
        #"""Aplica la expansión a todos los aliens en la formación."""
        self.expansion_elapsed += delta_time
        if self.expansion_elapsed >= self.expansion_duration:
            self.expansion_elapsed = 0.0

        progress = self.expansion_elapsed / self.expansion_duration
        expansion_progress = progress / 0.5 if progress < 0.5 else (1 - (progress - 0.5) / 0.5)

        for alien in self.aliens:
            if not alien.attack_mode:
                adjusted_index = self.get_adjusted_index(alien)
                sign = -1 if alien.is_left_alien() else 1
                max_offset = sign * 30 * ((adjusted_index + 1) / 4)

                # Aplicar modificaciones específicas por tipo
                if alien.alien_type == "red" and alien.mIndex in [0, 1, 2, 3]:
                    max_offset *= 0.5
                if alien.alien_type == "blue" and alien.mIndex in [16, 17, 18, 19]:
                    max_offset *= 0.5
                if alien.alien_type == "boss_green" and alien.mIndex in [36, 37]:
                    max_offset *= 0.5
                if alien.alien_type == "boss_green" and alien.mIndex in [38, 39]:
                    max_offset *= 2

                alien.expansion_offset = max_offset * expansion_progress
                alien.expansion_offset_y = 25 * expansion_progress
            else:
                # Si el alien está en modo ataque, restablecer los desplazamientos de expansión
                alien.expansion_offset = 0.0
                alien.expansion_offset_y = 0.0
       

    
        
        # Actualizar movimiento lateral del grid si está activo
        
    def update_arrival_phases(self, delta_time):
        
        # Actualiza las fases de llegada de los alienígenas        
        if self.current_phase == 0:
        # Fase 1: Alienígenas rojos 0-3
            if all(alien.arrived for alien in self.aliens if alien.mIndex in [0, 1, 2, 3]):
                self.current_phase += 1
                self.reset_start_time("blue", [0, 1, 2, 3])
               

        elif self.current_phase == 1:
            # Fase 2: Alienígenas azules 16-19
            if all(alien.arrived for alien in self.aliens if alien.mIndex in [16, 17, 18, 19]):
                self.current_phase += 1
                self.reset_start_time("red", [4, 5, 6, 7])
                self.reset_start_time("boss_green", [0, 1, 2, 3])
                    

        elif self.current_phase == 2:
            # Fase 3: Alienígenas rojos 4-7 y verdes 36-39
            if all(alien.arrived for alien in self.aliens if alien.mIndex in [4, 5, 6, 7, 36, 37, 38, 39]):
                self.current_phase += 1
                self.reset_start_time("red", range(8, 16), )
                

        elif self.current_phase == 3:
            # Fase 4: Alienígenas rojos 8-15
            if all(alien.arrived for alien in self.aliens if alien.mIndex in range(8, 16)):
                self.current_phase += 1
                self.reset_start_time("blue", range(4, 12))
                

        elif self.current_phase == 4:
            # Fase 5: Alienígenas azules 20-27
            if all(alien.arrived for alien in self.aliens if alien.mIndex in range(20, 28)):
                self.current_phase += 1
                self.reset_start_time("blue", range(12, 20))
                

        elif self.current_phase == 5:
            # Fase 6: Alienígenas azules 28-35
            if all(alien.arrived for alien in self.aliens if alien.mIndex in range(28, 36)):
                self.aliens_arrived = True
                # self.moving_to_center = True
                self.lateral_movement_active = False  # Detener el movimiento lateral de inmediato
                self.centering_time_elapsed = 0.0
                self.current_move_start = self.current_move
                self.expanding = True
           
    
    def update_lateral_movement(self, delta_time):
        """Actualiza el movimiento lateral del grid."""
        
        if self.lateral_movement_active:
                self.current_move += self.move_speed * delta_time * self.direction
                if abs(self.current_move) >= self.move_distance:
                    self.current_move = self.move_distance * self.direction
                    self.direction *= -1  # Cambiar dirección
        
    def apply_continuous_expansion(self, delta_time):
        """Aplica la expansión continua al grid."""
        if self.expanding:
            self.apply_expansion(delta_time)
            
    def define_attack_formations(self):
        # Definir las formaciones de ataque
        self.attack_formations = [
            ['red'],
            ['blue'],
            ['boss_green'],
            ['boss_blue'],
            ['boss_green', 'red'],
            ['boss_green', 'red', 'red'],
            ['boss_blue', 'red'],
            ['boss_blue', 'red', 'red']
            # Agrega más formaciones según necesites
        ]    
        # Cuanto mayor sea el peso, mayor será la probabilidad de selección
        self.attack_weights = [5, 1, 2, 2, 1, 1, 1, 1]  # Ajusta los pesos según tu preferencia

    
               
    def update_attack_phases(self, delta_time):
        if self.all_aliens_in_final_position():
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_interval:
                self.attack_timer = 0.0
                self.attack_interval = random.uniform(0.5, 1.0)
                # Seleccionar una formación de ataque al azar
                formation = random.choices(self.attack_formations, weights=self.attack_weights, k=1)[0]
                if formation == ['boss_green', 'red', 'red'] or formation == ['boss_green', 'red'] or formation == ['boss_blue', 'red'] or formation == ['boss_blue', 'red', 'red']:
                    self.initiate_combined_attack_formation(formation)
                elif formation == ['boss_green'] or formation == ['boss_blue']:
                    self.capture_formation(formation)
                elif formation == ['red'] or formation == ['blue']:
                    #self.capture_formation(formation)   
                    self.initiate_attack_formation(formation)
                
                    
 
 
 
    def capture_formation(self, formation):
        # Buscar alienígenas disponibles que coincidan con los tipos en la formación
        possible_aliens = [alien for alien in self.aliens if alien.alien_type in formation and not alien.attack_mode and alien.arrived]

        if not possible_aliens:
            return

        attack_group = []

        for alien_type in formation:
            aliens_of_type = [alien for alien in possible_aliens if alien.alien_type == alien_type]
            if aliens_of_type:
                # Seleccionar un alienígena al azar del tipo especificado
                alien_to_attack = random.choice(aliens_of_type)
                attack_group.append(alien_to_attack)
                possible_aliens.remove(alien_to_attack)
            else:
                # No hay suficientes alienígenas de este tipo
                return

        # Iniciar ataque para el grupo
        for alien in attack_group:
            alien.attack_mode = True
            alien.is_capture_formation = True  # Indicar que es una formación de captura

            if alien.alien_type == 'boss_green' or alien.alien_type == 'boss_blue':
                # Definir curvas de captura específicas para boss_green
                if alien.mIndex % 2 == 0:
                    alien.capture_player.define_capture_curves_1()
                else:
                    alien.capture_player.define_capture_curves_2()
            # elif alien.alien_type == 'red':
            #     # Definir curvas de ataque para red aliens
            #     if alien.mIndex % 2 == 0:
            #         alien.define_attack_curves_1_1()
            #     else:
            #         alien.define_attack_curves_2_1()

 
    def initiate_attack_formation(self, formation):
        # formation es una lista de tipos de alienígenas, por ejemplo ['boss_green', 'red', 'red']
        possible_aliens = [alien for alien in self.aliens if alien.alien_type in formation and not alien.attack_mode and alien.arrived]
        
        if not possible_aliens:
            return  # No hay alienígenas disponibles para esta formación

        attack_group = []

        for alien_type in formation:
            # Encontrar los alienígenas de este tipo más alejados del jugador
            aliens_of_type = [alien for alien in possible_aliens if alien.alien_type == alien_type]
            if aliens_of_type:
                player_x, player_y = self.game.player_sprite.rect.center
                # Ordenar los alienígenas por distancia al jugador (de mayor a menor)
                aliens_of_type.sort(key=lambda alien: ((alien.x - player_x)**2 + (alien.y - player_y)**2), reverse=True)
                # Seleccionar los dos más alejados, o menos si no hay suficientes
                farthest_aliens = aliens_of_type[:3]
                if farthest_aliens:
                # Elegir uno de los dos de forma aleatoria para atacar
                    alien_to_attack = random.choice(farthest_aliens)
                    attack_group.append(alien_to_attack)
                    possible_aliens.remove(alien_to_attack)
            else:
                # No hay suficientes alienígenas disponibles de este tipo
                return

        # Iniciar ataque para el grupo
        for alien in attack_group:
            alien.attack_mode = True
            alien.is_capture_formation = False  # No es una formación de captura
            # Aplicar la curva según si el índice del alien es par o impar
            if alien.mIndex % 2 == 0:  # Si el índice es par
                alien.define_attack_curves_2()
                
            else:  # Si el índice es impar
                #alien.define_attack_curves_3()
                self.initiate_red_attack_group_1()
                
                
    def initiate_combined_attack_formation(self, formation):
        # Obtener los índices de las formaciones específicas
        formations_indices = [
            [38, 8, 4],
            [36, 4, 0],
            [37, 1, 5],
            [39, 5, 9]
        ]

        possible_aliens = [alien for alien in self.aliens if not alien.attack_mode and alien.arrived]

        if not possible_aliens:
            return

        player_x, player_y = self.game.player_sprite.rect.center
        farthest_group = None
        farthest_distance = -float('inf')

        for indices in formations_indices:
            aliens_in_formation = [alien for alien in possible_aliens if alien.mIndex in indices]

            # Verificar que los alienígenas en la formación coincidan con el tipo especificado
            formation_types = [alien.alien_type for alien in aliens_in_formation]
            if sorted(formation_types) == sorted(formation):
                # Calcular la distancia promedio al jugador
                avg_distance = sum(
                    ((alien.x - player_x) ** 2 + (alien.y - player_y) ** 2) ** 0.5
                    for alien in aliens_in_formation
                ) / len(aliens_in_formation)

                if avg_distance > farthest_distance:
                    farthest_group = aliens_in_formation
                    farthest_distance = avg_distance

        if farthest_group:
            # Calcular el centro del grupo
            group_center_x = sum(alien.x for alien in farthest_group) / len(farthest_group)
            group_center_y = sum(alien.y for alien in farthest_group) / len(farthest_group)

            # Preparar a cada alienígena en el grupo
            for alien in farthest_group:
                # Restablecer los desplazamientos de expansión
                alien.expansion_offset = 0.0
                alien.expansion_offset_y = 0.0

                # Establecer la posición del alienígena en su posición objetivo inicial
                alien.x = alien.initial_target_x
                alien.y = alien.initial_target_y

                alien.attack_mode = True
                alien.is_capture_formation = False  # No es una formación de captura

                # Calcular el desplazamiento relativo en X e Y para cada alienígena
                relative_offset_x = alien.initial_target_x - group_center_x
                relative_offset_y = alien.initial_target_y - group_center_y

                # Asignar la curva adecuada según si el alienígena es par o impar
                if alien.mIndex % 2 == 0:
                    # Alienígenas pares usan define_attack_curves_relative
                    alien.curvas_relativas.define_attack_curves_relative(relative_offset_x, relative_offset_y)
                else:
                    # Alienígenas impares usan define_attack_curves_relative_2
                    alien.curvas_relativas.define_attack_curves_relative_2(relative_offset_x, relative_offset_y)


                            
                    
    def initiate_red_attack_group_1(self):
        """Inicia el ataque para el grupo 1 de alienígenas rojos."""
        red_aliens_group_1 = [alien for alien in self.aliens]
        if red_aliens_group_1:
            attacking_alien = random.choice(red_aliens_group_1)
            attacking_alien.attack_mode = True
            attacking_alien.define_attack_curves()
    
    def initiate_boss_green_attack_group_1(self):
        """Inicia el ataque para el grupo 1 de alienígenas rojos."""
        boss_green_aliens_group_1 = [alien for alien in self.aliens if alien.mIndex in [36, 39]]
        if boss_green_aliens_group_1:
            attacking_alien = random.choice(boss_green_aliens_group_1)
            attacking_alien.attack_mode = True
            attacking_alien.define_attack_curves_2()   
            
                
            
        
            
    def apply_lateral_movement_to_aliens(self):
        """Aplica el movimiento lateral del grid a cada alienígena."""
        if not self.expanding:
            for alien in self.aliens:
                alien.grid_offset_x = self.current_move        
                        

    def reset_start_time(self, alien_type, bezier_id):
        """Reinicia el tiempo de inicio para los alienígenas especificados."""
        for alien in self.aliens:
            if alien.alien_type == alien_type and alien.bezier_id in bezier_id:
                alien.time_since_start = 0.0

    def draw(self, surface):
        for alien in self.aliens:
            alien.draw(surface)
            
        
    
    def update(self, delta_time):
        
        # Actualizar movimiento lateral
        self.update_lateral_movement(delta_time)
        
        # Actualizar fases de llegada
        self.update_arrival_phases(delta_time)
        
        # Aplicar expansión continua
        self.apply_continuous_expansion(delta_time)
        
        self.apply_lateral_movement_to_aliens()
        
        # Actualizar fases de ataque
        self.update_attack_phases(delta_time)
        
        # # Actualizar la lógica de cada alienígena
        self.aliens.update(delta_time)
        
       

if __name__ == "__main__":
    game = Game()
    game.run()