import pygame
import sys
import os
import numpy as np
import random
import time
from player import *
from laser import *
from explosion import *

# Clase Game
class Game:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()

        # Configuración de la ventana
        self.WINDOW_WIDTH = 650
        self.WINDOW_HEIGHT = 950
        self.SPRITE_SIZE = 16
        self.PLAYER_SIZE = (45, 45)
        self.explosion_size = (90, 90)
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Formación de Alienígenas con Expansión Continua")
        self.sprite_explotion_coord = [(289, 1, 32, 32), (323,1, 32, 32),(357,1, 32, 32),(391,1, 32, 32), (425,1, 32, 32)]

        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        
        # Puntaje
        self.score = 0  # Iniciar el puntaje en 0
        self.high_score = self.load_high_score()
        
        # Fuente para mostrar el puntaje
        self.FONT_score = pygame.font.Font('asset\emulogic\emulogic.ttf', 20)

        # Fuente para mostrar el mIndex
        self.FONT = pygame.font.SysFont(None, 24)

        # Cargar la hoja de sprites con la ruta actualizada
        self.SPRITE_SHEET = pygame.image.load(r"E:\Python Pygame\Python Test_6\asset\Galaga_SpritesSheet.png")

        self.background_2 = Background_2(self)

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
        self.last_time = time.time()
        
    def get_sprite(self, coordinates):
        """Extrae el sprite de la hoja de sprites dado un rectángulo de coordenadas."""
        x, y, width, height = coordinates
        sprite = pygame.Surface((width, height))
        sprite.blit(self.SPRITE_SHEET, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return pygame.transform.scale(sprite, (40, 40))
    
    def check_for_collision(self):
        for laser_sprite in self.player_group.sprite.laser_group:
            # Verificar colisiones usando pygame.sprite.collide_mask
            collisions = pygame.sprite.spritecollide(laser_sprite, self.formation.aliens, False, pygame.sprite.collide_mask)
            for alien in collisions:
                # Eliminar el láser y el alienígena cuando colisionan
                explosion_position = alien.rect.center
                
                alien_type = alien.alien_type

                # Asignar puntos según el color del alien
                if alien_type == "red":
                    self.score += 80
                elif alien_type == "blue":
                    self.score += 50
                elif alien_type == "boss_green":
                    self.score += 150
                
                
                laser_sprite.kill()  
                alien.kill()
                
                self.explosion_sprite = Explosion(self.SPRITE_SHEET, self.sprite_explotion_coord, self.explosion_size)
                self.explosion_sprite.start_explosion(explosion_position)
                self.explosion_group.add(self.explosion_sprite)
                
                
                self.explosion_sprite.start_explosion(explosion_position)           
                # self.hit_count += 1
                # if self.hit_count == 1:
                #     #sprite.cambiar_sprite()  
                #     laser_sprite.kill()
                # elif self.hit_count >= 3:
                #     sprite.kill()
                #     laser_sprite.kill()
                #     #self.explosion_sprite.update(sprite.rect)
                #     self.hit_count = 0
 
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
 
 
    def draw_score(self):
        # Dibuja el puntaje actual en la pantalla.
        score_text = self.FONT_score.render("1UP", True, self.RED)
        score_text_2 = self.FONT_score.render(f"{self.score}", True, self.WHITE)
        score_text_3 = self.FONT_score.render("HIGH SCORE", True, self.RED)
        high_score_text = self.FONT_score.render(f"{self.high_score}", True, self.WHITE)
        
        # Posiciones fijas para 1UP y puntaje actual
        self.SCREEN.blit(score_text, (30, 15))
        self.SCREEN.blit(score_text_2, (50, 45))
        
        # Posición fija para "HIGH SCORE"
        score_text_3_x = 250
        
        
        # Calcular la posición centrada para high_score_text en relación a "HIGH SCORE"
        score_text_3_width = score_text_3.get_width()  # Ancho del texto "HIGH SCORE"
        high_score_text_width = high_score_text.get_width()  # Ancho del high score
        centered_high_score_x = score_text_3_x + ((score_text_3_width - high_score_text_width) // 2) - high_score_text_width/2
        
         # Calcular la posición centrada para high_score_text en relación a SCORE
        score_text_width = score_text.get_width()  # Ancho del texto "1 UPE"
        score_text_2_width = score_text_2.get_width()  # Ancho del high score
        centered_score_x = score_text_3_x + (score_text_2_width - high_score_text_width) // 2
        
        
        # Dibujar high_score_text centrado
        self.SCREEN.blit(high_score_text, (centered_high_score_x, 45))
        self.SCREEN.blit(score_text_3, (centered_score_x, 15))
    
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
        running = True

        while running:
            # Calcular delta_time
            delta_time = self.calculate_delta_time()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    running = False

            # Actualizar lógica de la formación
                  
            self.formation.update (delta_time)
            self.background_2.update(delta_time)
            self.player_group.update(delta_time)
            self.check_for_collision()
            self.check_high_score()  # Verificar si el score actual supera el high score
            
            # Dibujar
            self.SCREEN.fill(self.BLACK)
            self.background_2.draw()
            self.formation.draw(self.SCREEN)
            self.player_group.draw(self.SCREEN)
            self.player_sprite.laser_group.draw(self.SCREEN)
            self.draw_score()
            # Actualizar y dibujar explosiones
            self.explosion_group.update(delta_time)
            self.explosion_group.draw(self.SCREEN)
           
            # Actualizar la pantalla
            pygame.display.flip()

        # Salir de Pygame
        pygame.quit()
        sys.exit()

class Background_2:
    def __init__(self, game ):
        self.game = game
        self.screen = pygame.display.get_surface()
        self.scroll_speed = 1.6
        self.toggle_interval = 40
        self.toggle_timer = 0
        self.show_first_half = True
        self.background_y = 0
        
        self.colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (128, 128, 128)]  # rojo, azul, amarillo, gris
        self.rects = self.generate_rects(80)
        self.first_half, self.second_half = self.split_rects()

    def generate_rects(self, num_rects):
        rects = []
        for _ in range(num_rects):
            x = random.randint(0, self.game.WINDOW_WIDTH - 4)
            y = random.randint(0, self.game.WINDOW_HEIGHT - 4)
            color = random.choice(self.colors)
            rects.append((pygame.Rect(x, y, 2, 1), color))
        return rects

    def split_rects(self):
        half_index = len(self.rects) // 2
        return self.rects[:half_index], self.rects[half_index:]

    def update(self, delta_time):
        self.background_y += self.scroll_speed
        if self.background_y >= self.game.WINDOW_HEIGHT:
            self.background_y = 0

        self.toggle_timer += delta_time * 200
        if self.toggle_timer >= self.toggle_interval:
            self.show_first_half = not self.show_first_half
            self.toggle_timer = 0

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fondo negro

        if self.show_first_half:
            for rect, color in self.first_half:
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y - self.game.WINDOW_HEIGHT))
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y))
        else:
            for rect, color in self.second_half:
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y - self.game.WINDOW_HEIGHT))
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y))

    def draw_rect(self, rect, color):
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill(color)
        return surface





# Clase Alien
class Alien(pygame.sprite.Sprite):
    # Variables de clase para la animación
    animation_frames = []
    global_animation_timer = 0.0
    global_animation_interval = 20  # Intervalo entre frames en segundos
    global_animation_index = 0

    # Variables de clase para los sprites
    animation_frames_by_type = {
        "red": [],
        "blue": [],
        "boss_green": []
    }

    def __init__(self, mIndex, formation, alien_type, bezier_id):
        super().__init__()  # Inicializar la clase base de pygame.sprite.Sprite
        self.mIndex = mIndex
        self.bezier_id = bezier_id 
        self.formation = formation  # Referencia a la formación
        self.alien_type = alien_type
        self.speed = 1.8  # Velocidad a lo largo de la curva
        self.t = 0.0  # Parámetro para recorrer la curva
        self.curve_index = 0  # Índice de la curva actual
        self.arrived = False  # Indica si el alien ha llegado a su posición objetivo
        self.time_since_start = 0.0  # Tiempo acumulado desde el inicio
        self.active = False  # Indica si el alien está activo
        self.angle = 0.0  # Ángulo de rotación
        
        # Nuevas variables para controlar el comportamiento en la curva Bézier
        self.curve_start_delay = 0.05 * bezier_id  # Retraso en el inicio de la curva
        self.curve_spacing_factor = 1.0  # Factor de separación en la curva
        self.curve_speed_factor = 1.0  # Factor de velocidad en la curva

        # Posición objetivo inicial
        # En la clase Alien, método __init__:

        self.initial_target_x, self.initial_target_y = self.formation.get_initial_target_position(self.mIndex)

        # Desplazamiento del grid
        self.grid_offset_x = 0.0

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
            elif self.alien_type == "boss_blue":
                Alien.animation_frames_by_type["boss_blue"] = [
                    self.formation.game.get_sprite((109, 55, 16, 16)),
                    self.formation.game.get_sprite((127, 55, 16, 16))
                ]


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
                self.control_points(),
                self.control_points_2()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)
        elif self.mIndex in [28, 29, 30, 31, 32, 33, 34, 35]:
            self.curves = [
                self.control_points_12(),
                self.control_points_13()
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
        width = self.formation.game.WINDOW_WIDTH
        return np.array([
            [width / 2 - 20, -10],
            [width / 2 - 10, 260],
            [width - 10, 305],
            [width - 65, 470]
        ])

    def control_points_2(self):
        width = self.formation.game.WINDOW_WIDTH
        return np.array([
            [width - 65, 470],
            [width - 98, 543],
            [width / 2 + 10, 480],
            [width / 2 - 10, 330]
        ])
    def control_points_3(self):
        # Puntos de control originales para aliens 4-7
        return (
            np.array([-5, 706]),
            np.array([205, 659]),
            np.array([263, 524]),
            np.array([212, 463])
        )

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
            np.array([212, 463])
        )

    def control_points_6(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([width + 5, 706]),
            np.array([width - 205, 659]),
            np.array([width - 263, 524]),
            np.array([width - 212, 463])
        )

    def control_points_7(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([width - 212, 463]),
            np.array([width - 163, 356]),
            np.array([width - 15, 410]),
            np.array([width - 56, 517])
        )

    def control_points_8(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([width - 56, 517]),
            np.array([width - 123, 619]),
            np.array([width - 248, 561]),
            np.array([width - 212, 463])
        )

    def control_points_9(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([width / 2 + 20, -10]),
            np.array([width / 2 + 10, 260]),
            np.array([10, 305]),
            np.array([65, 470])
        )
    def control_points_10(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([65, 470]),
            np.array([98, 543]),
            np.array([width / 2 + 10, 480]),
            np.array([width / 2 + 5, 400])
        )    
    

    def control_points_11(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([width  / 2 - 20, -10]),
            np.array([width  / 2 - 10, 260]),
            np.array([width  - 10, 305]),
            np.array([width  - 65, 470])
        )

    def control_points_12(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([width / 2 + 20, -10]),
            np.array([width / 2 + 10, 260]),
            np.array([10, 305]), np.array([65, 470])
        )
    def control_points_13(self):
        width = self.formation.game.WINDOW_WIDTH
        return (
            np.array([65, 470]), np.array([98, 543]),
            np.array([width / 2 + 10, 480]),
            np.array([width / 2 + 5, 400])

        )
    # ... Otros métodos de puntos de control no han cambiado ...

    def bezier_curve(self, points, t):
        """Calcula el punto en la curva Bézier cúbica para un valor de t dado."""
        return (
            (1 - t) ** 3 * points[0] +
            3 * (1 - t) ** 2 * t * points[1] +
            3 * (1 - t) * t ** 2 * points[2] +
            t ** 3 * points[3]
        )

    # def bezier_derivative(self, points, t):
    #     """Calcula la derivada en la curva Bézier cúbica para un valor de t dado."""
    #     return (
    #         3 * (1 - t) ** 2 * (points[1] - points[0]) +
    #         6 * (1 - t) * t * (points[2] - points[1]) +
    #         3 * t ** 2 * (points[3] - points[2])
    #     )

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
    def animar_los_bichos(cls, delta_time):
        cls.global_animation_timer += delta_time
        if cls.global_animation_timer >= cls.global_animation_interval:
            cls.global_animation_timer -= cls.global_animation_interval

            # Ajustar global_animation_index para no exceder el tamaño de los frames de animación
            max_index = len(cls.animation_frames_by_type["red"])  # Suponemos que todos tienen la misma cantidad de frames
            cls.global_animation_index = (cls.global_animation_index + 1) % max_index



    def update(self, delta_time):
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
                # Fase 4: Alienígenas rojos 8-15
                if self.time_since_start >= self.start_delay - 1:
                    self.active = True

            elif current_phase == 4 and self.mIndex in range(20, 28):
                # Fase 5: Alienígenas azules 20-27
                if self.time_since_start >= self.start_delay:
                    self.active = True

            elif current_phase == 5 and self.mIndex in range(28, 36):
                # Fase 6: Alienígenas azules 28-35
                if self.time_since_start >= self.start_delay - 2 :
                    self.active = True

        if self.active and not self.arrived:
            
                   
            
            self.t += (self.speed * self.curve_speed_factor * delta_time * self.curve_spacing_factor)
            if self.t > 1.0:
                self.t = 1.0
            # Obtener los puntos de control para la curva actual
            points = self.curves[self.curve_index]
            # Para la última curva, ajustar el último punto de control a la posición objetivo actual
            if self.curve_index == len(self.curves) - 1:
                target_x = self.initial_target_x + self.grid_offset_x
                target_y = self.initial_target_y
                # Ajuste de precisión del último punto de control para que coincida exactamente con el objetivo
                points = list(points)  # Convertir a lista para modificar
                points[-1] = np.array([target_x, target_y])
                points = np.array(points)
            else:
                points = np.array(points)
            
            # Calcular posición y derivada
            position = self.bezier_curve(points, self.t)
            derivative = self.bezier_derivative(points, self.t)
            self.x, self.y = position
            
            # Calcular el ángulo para la rotación
            dx, dy = derivative
            angle = np.degrees(np.arctan2(dy, dx))
            self.angle = angle + 90
            if self.t >= 1.0:
                self.t = 0.0
                self.curve_index += 1
                if self.curve_index >= len(self.curves):
                    # Ha terminado todas las curvas
                    self.arrived = True
                    # Ajustar posición final a la posición objetivo actual del grid
                    self.x = self.initial_target_x + self.grid_offset_x
                    self.y = self.initial_target_y
                    self.angle = 0.0  # Restablecer ángulo
                    
                    
        elif self.arrived:
            # Actualizar la posición durante la expansión
            self.x = self.initial_target_x + self.grid_offset_x + self.expansion_offset
            self.y = self.initial_target_y + self.expansion_offset_y
            self.angle = 0.0  # Sin rotación al llegar


        rotated_image = pygame.transform.rotate(self.animation_frames[Alien.global_animation_index], -self.angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        
        # Asegúrate de actualizar la máscara después de cada cambio
        self.mask = pygame.mask.from_surface(self.image)

        # Actualizar la animación global
        Alien.animar_los_bichos(delta_time)
        if 0 <= Alien.global_animation_index < len(self.animation_frames):
            self.image = self.animation_frames[Alien.global_animation_index]
            

    def draw(self, surface):
        if self.active or self.arrived:
            # Obtener el frame de animación actual
            self.image = self.animation_frames[Alien.global_animation_index]
            # Rotar la imagen
            self.rotated_image = pygame.transform.rotate(self.image, -self.angle)
            rect = self.rotated_image.get_rect(center=(int(self.x), int(self.y)))
            
            surface.blit(self.rotated_image, rect)
            #Renderizar el texto del mIndex
            text = self.formation.game.FONT.render(str(self.mIndex), True, self.formation.game.WHITE)
            text_rect = text.get_rect(center=(int(self.x), int(self.y) + 30))
            #surface.blit(text, text_rect)
            
        

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

        # Variables para el movimiento suave al centro
        self.moving_to_center = False
        self.centering_duration = 1.0  # Duración para moverse al centro (en segundos)
        self.centering_time_elapsed = 0.0
        self.current_move_start = 0.0  # Valor inicial de current_move al comenzar a centrar

        # Movimiento lateral después de que los aliens hayan llegado
        self.aliens_arrived = False  # Indica si todos los aliens han llegado

        self.initial_target_positions = []  # Posiciones objetivo iniciales (sin movimiento)
        self.create_formation()

        # Variables para el patrón de expansión continuo
        self.expanding = False
        self.expansion_duration = 2.0  # Duración total de cada ciclo de expansión
        self.expansion_elapsed = 0.0
        self.expansion_delay = 1.0  # Retraso antes de iniciar la primera expansión

        # Fases de llegada de alienígenas
        self.current_phase = 0  # Índice de la fase actual

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
            alien = Alien(mIndex + offset, self, alien_type, bezier_id)
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
            col = mIndex // 2  # `0` o `1` para cada par de alienígenas en el lado izquierdo y derecho
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
            screen_x = retVal_x + self.game.WINDOW_WIDTH // 2
            screen_y = retVal_y + 180  # Posición objetivo en Y
            
            if alien_type == "blue":
                screen_y += 70
            # elif alien_type == "boss_green":
            #     screen_y += 350
            return int(screen_x), int(screen_y)
        
        # Ajustar posiciones para la pantalla para los alienígenas verdes
        screen_x = retVal_x + self.game.WINDOW_WIDTH // 2
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
            
        adjusted_index = group
        return adjusted_index

    def update(self, delta_time):
        
        # Actualizar movimiento lateral del grid si está activo
        if self.lateral_movement_active:
            self.current_move += self.move_speed * delta_time * self.direction
            if abs(self.current_move) >= self.move_distance:
                self.current_move = self.move_distance * self.direction
                self.direction *= -1  # Cambiar dirección
            
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
        


        # Manejar la expansión continua
        if self.expanding:
            self.expansion_elapsed += delta_time
            if self.expansion_elapsed >= self.expansion_duration:
                self.expansion_elapsed = 0.0
              

            progress = self.expansion_elapsed / self.expansion_duration
            if progress < 0.5:
                expansion_progress = progress / 0.5  # Expansión de 0 a 1
            else:
                expansion_progress = (1 - (progress - 0.5) / 0.5)  # Contracción de 1 a 0

            # Aplicar el movimiento de expansión a cada alienígena
            for alien in self.aliens:
                adjusted_index = self.get_adjusted_index(alien)
                sign = -1 if alien.is_left_alien() else 1
                max_offset = sign * 30 * ((adjusted_index + 1) / 4)

                # Aplicar modificaciones específicas según el tipo de alienígena
                if alien.alien_type == "red" and alien.mIndex in [0, 1, 2, 3]:
                    max_offset *= 0.5
                if alien.alien_type == "blue" and alien.mIndex in [16, 17, 18, 19]:
                    max_offset *= 0.5
                if alien.alien_type == "boss_green" and alien.mIndex in [36, 37]:
                    max_offset *= 0.5
                if alien.alien_type == "boss_green" and alien.mIndex in [38, 39]:
                    max_offset *= 2

                alien.expansion_offset = max_offset * expansion_progress

                # Calcular el desplazamiento vertical constante
                max_offset_y = 25  # Desplazamiento vertical constante
                alien.expansion_offset_y = max_offset_y * expansion_progress

               
        # Actualizar cada alienígena con el movimiento lateral del grid si no estamos centrando ni expandiendo
        if not self.moving_to_center and not self.expanding:
            for alien in self.aliens:
                alien.grid_offset_x = self.current_move

       
        
        
        # Actualizar la lógica de cada alienígena
        self.aliens.update(delta_time)

    def reset_start_time(self, alien_type, bezier_id):
        """Reinicia el tiempo de inicio para los alienígenas especificados."""
        for alien in self.aliens:
            if alien.alien_type == alien_type and alien.bezier_id in bezier_id:
                alien.time_since_start = 0.0

    

    def draw(self, surface):
        for alien in self.aliens:
            alien.draw(surface)
            
       
        

if __name__ == "__main__":
    game = Game()
    game.run()
