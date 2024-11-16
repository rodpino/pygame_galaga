import pygame
import numpy as np
import random
from entities.capture_player import CapturePlayer
from entities.alien_laser import AlienLaser
from settings import Settings
from entities.curvas_control import Alien_attack_curves
from entities.curvas_control import Relative_curves

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
        self.width = self.game.settings.WIDTH
        self.alien_attack_curves = Alien_attack_curves(self)
        
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
        self.curvas_relativas = Relative_curves (self, formation, game)
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
                    self.game.resources.get_sprite((109, 73, 16, 16), (self.game.settings.ALIENS_SIZE)),
                    self.game.resources.get_sprite((127, 73, 16, 16), (self.game.settings.ALIENS_SIZE))
                ]
            elif self.alien_type == "blue":
                Alien.animation_frames_by_type["blue"] = [
                    self.game.resources.get_sprite((109, 91, 16, 16), (self.game.settings.ALIENS_SIZE)),
                    self.game.resources.get_sprite((127, 91, 16, 16), (self.game.settings.ALIENS_SIZE))
                ]
            elif self.alien_type == "boss_green":
                Alien.animation_frames_by_type["boss_green"] = [
                    self.game.resources.get_sprite((109, 37, 16, 16), (self.game.settings.ALIENS_SIZE)),
                    self.game.resources.get_sprite((127, 37, 16, 16), (self.game.settings.ALIENS_SIZE))
                ]
                Alien.animation_frames_by_type["boss_blue"] = [
                    self.game.resources.get_sprite((109, 55, 16, 16), (self.game.settings.ALIENS_SIZE)),
                    self.game.resources.get_sprite((127, 55, 16, 16), (self.game.settings.ALIENS_SIZE))
                ]

        if not self.capture_animation_frames:
            self.capture_animation_frames = [
            self.game.resources.get_sprite((289, 36, 48, 80), self.game.settings.CAPTURE_SIZE),
            self.game.resources.get_sprite((339, 36, 48, 80), self.game.settings.CAPTURE_SIZE),
            self.game.resources.get_sprite((389, 36, 48, 80), self.game.settings.CAPTURE_SIZE)
        ]
        
            
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
                self.game.grid_formation_curves.control_points_1(),
                self.game.grid_formation_curves.control_points_2()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = self.bezier_id * 0.2
        elif self.mIndex in [4, 5, 6, 7]:
            self.curves = [
                self.game.grid_formation_curves.control_points_3(),
                self.game.grid_formation_curves.control_points_4(),
                self.game.grid_formation_curves.control_points_5()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = self.bezier_id * 0.25
        elif self.mIndex in [8, 9, 10, 11, 12, 13, 14, 15]:
            self.curves = [
                self.game.grid_formation_curves.control_points_6(),
                self.game.grid_formation_curves.control_points_7(),
                self.game.grid_formation_curves.control_points_8()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)

    def define_blue_curves(self):
        """Define las curvas específicas para los alienígenas azules."""
        if self.mIndex in [16, 17, 18, 19]:
            self.curves = [
                self.game.grid_formation_curves.control_points_12(),
                self.game.grid_formation_curves.control_points_13()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)
        elif self.mIndex in [20, 21, 22, 23, 24, 25, 26, 27]:
            self.curves = [
                self.game.grid_formation_curves.control_points_14(),
                self.game.grid_formation_curves.control_points_15()
            ]
            self.start_x, self.start_y = self.curves[0][0]
            self.start_delay = (self.bezier_id * 0.2)
        elif self.mIndex in [28, 29, 30, 31, 32, 33, 34, 35]:
            self.curves = [
                self.game.grid_formation_curves.control_points_10(),
                self.game.grid_formation_curves.control_points_11()
            ]
        self.start_x, self.start_y = self.curves[0][0]
        self.start_delay = (self.bezier_id * 0.2)
        
    def define_boss_green_curves(self):
        """Define las curvas específicas para los alienígenas azules."""
        if self.mIndex in [36, 37, 38, 39]:
            self.curves = [
                self.game.grid_formation_curves.control_points_3(),
                self.game.grid_formation_curves.control_points_4(),
                self.game.grid_formation_curves.control_points_5()
            ]
           
        self.start_x, self.start_y = self.curves[0][0]
        self.start_delay = (self.bezier_id * 0.25 + 0.88)




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
                self.alien_attack_curves.attack_control_points_1_1(offset_x),
                self.alien_attack_curves.attack_control_points_1_2(offset_x),
                self.alien_attack_curves.attack_control_points_1_3(offset_x),
                self.alien_attack_curves.attack_control_points_1_4(offset_x)
            ]
            
    def define_attack_curves_2_1(self, offset_x=0):
        if self.alien_type == "red"or "blue":
            self.attack_curves = [
                self.alien_attack_curves.attack_control_points_2_1(offset_x),
                self.alien_attack_curves.attack_control_points_2_2(offset_x),
                self.alien_attack_curves.attack_control_points_2_3(offset_x),
                self.alien_attack_curves.attack_control_points_2_4(offset_x)
            ]

    def define_attack_curves(self, offset_x=0):
        if self.alien_type == "blue":
            self.attack_curves = [
                self.alien_attack_curves.attack_control_points_1_1(offset_x),
                self.alien_attack_curves.attack_control_points_1_2(offset_x),
                self.alien_attack_curves.attack_control_points_1_3(offset_x),
                self.alien_attack_curves.attack_control_points_1_4(offset_x)
            ]

    def define_attack_curves_2(self, offset_x=0 ) : 
        random_xx =  random.randint(-50, 120)
        if self.alien_type == "blue":
            self.attack_curves = [
                self.alien_attack_curves.attack_control_points_4(random_xx, offset_x),
                self.alien_attack_curves.attack_control_points_5(random_xx, offset_x),
                self.alien_attack_curves.attack_control_points_6(random_xx, offset_x)
                
            ]

    def define_attack_curves_3(self, offset_x=0):
        random_xx =  random.randint(-150, 50)
        if self.alien_type == "blue":
            self.attack_curves = [
                self.alien_attack_curves.attack_control_points_8(random_xx, offset_x),
                self.alien_attack_curves.attack_control_points_9(random_xx, offset_x),
                self.alien_attack_curves.attack_control_points_10(random_xx, offset_x)
            
        ]

        
    def define_attack_curves_4(self, offset_x=0):
        self.attack_curves = [
            
            self.alien_attack_curves.attack_control_points_11(offset_x),
            self.alien_attack_curves.attack_control_points_12(offset_x)
        ]       


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


    
    def shoot(self, delta_time):
        current_time = pygame.time.get_ticks()
        if self.attack_mode and self.curve_attack_index <=  1: 
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.last_shot_time = current_time
                if random.random() < 0.1:  # Probabilidad de disparo
                    # Pasar la posición del jugador al láser
                    player_position = self.formation.game.player.rect.center
                    
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
        if self.alien_type == 'red' or self.alien_type == 'boss_blue':
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
                self.game.capture_light_group.update(frame_rect)
                #surface.blit(animation_frame, frame_rect)
            
            #Renderizar el texto del mIndex
            text = self.formation.game.FONT.render(str(self.mIndex), True, self.game.settings.WHITE)
            text_rect = text.get_rect(center=(int(self.x), int(self.y)))
            #surface.blit(text, text_rect)
            
        #self.game.resources.draw_bezier_path(surface)
        #self.debug_2(surface)
