import pygame
import os
from entities.player import Player


class Resources:
    def __init__(self, game):
        """Clase para manejar recursos del juego."""
        self.game = game
        self.SPRITE_SHEET = pygame.image.load(r"asset/Galaga_SpritesSheet.png")
        self.screen = pygame.display.get_surface()
        
        # Puntaje
        self.score = 0  # Iniciar el puntaje en 0
        self.high_score = self.load_high_score()
        
        # Puntaje
        self.score = 0  # Iniciar el puntaje en 0
        self.high_score = self.load_high_score()
         # Fuente para mostrar el puntaje
        self.FONT_score = pygame.font.Font('asset/fonts/emulogic.ttf', 20)

        # Fuente para mostrar el mIndex
        self.FONT = pygame.font.SysFont(None, 30)
        self.font = pygame.font.Font("asset/fonts/emulogic.ttf", 8)
        
        # Fuente para mostrar el puntaje
        self.FONT_score = pygame.font.Font('asset/fonts/emulogic.ttf', 20)
        

    def get_sprite(self, coordinates, sprite_size):
        """Extrae el sprite de la hoja de sprites dado un rectángulo de coordenadas."""
        x, y, width, height = coordinates
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.SPRITE_SHEET, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        sprite = sprite.convert_alpha()
        return pygame.transform.scale(sprite, (sprite_size))
        
    def check_for_collision(self):
        
        for player in self.game.player_group:
            for laser_sprite in player.game.player.laser_group:
                # Verificar colisiones usando pygame.sprite.collide_mask
                collisions = pygame.sprite.spritecollide(laser_sprite, self.game.formation.aliens, False, pygame.sprite.collide_mask)

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
                    self.game.explosion.start_explosion(explosion_position)
                    self.game.explosion_group.add(self.game.explosion)
                    
                # Eliminar el láser después de cada colisión 
                    laser_sprite.kill()
                
        
        for alien_sprite in self.game.formation.aliens:
                                
            if pygame.sprite.spritecollide(self.game.player, alien_sprite.laser_group, True, pygame.sprite.collide_mask):
                # Reducir una vida
                self.game.player.lives -= 1
                if self.game.player.lives <= 0:
                    self.game.player.lives = 0
                                   
                    
            if pygame.sprite.spritecollide(self.game.player, self.game.formation.aliens, True, pygame.sprite.collide_mask):
                # Reducir una vida
                self.game.player.lives -= 1
                # Verificar si el jugador ha perdido todas las vidas
                if self.game.player.lives <= 0:
                    self.game.player.lives = 0
                    
        if pygame.sprite.spritecollide(self.game.player, self.game.capture_light_group, False):
            if not self.game.player.has_clone:
                # Crear el clon a la derecha del jugador original
                clone_x = player.rect.right + 5
                clone_y = player.rect.centery
                player_clone = Player(self.game, x=clone_x, y=clone_y)
                player.has_clone = True
                self.game.player_group.add(player_clone)
                
        
        
            
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
    
    def game_over(self):
        
        game_over_text = self.FONT_score.render("Game Over", True, self.game.settings.RED)
        
        centered_text_whidt = game_over_text.get_width()
        centered_text = (self.game.settings.WIDTH/2) - (centered_text_whidt // 2)
        self.screen.blit(game_over_text, (centered_text, 500))
        
        
    def draw_score(self):
        # Dibuja el puntaje actual en la pantalla.
        score_text = self.FONT_score.render("1UP", True, self.game.settings.RED)
        score_text_2 = self.FONT_score.render(f"{self.score}", True, self.game.settings.WHITE)
        high_score_text_3 = self.FONT_score.render("HIGH SCORE", True, self.game.settings.RED)
        high_score_text = self.FONT_score.render(f"{self.high_score}", True, self.game.settings.WHITE)
        
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
        self.screen.blit(high_score_text_3, (score_text_3_x, 15))
        self.screen.blit(high_score_text, (centered_high_score_x, 45))
        self.screen.blit(score_text, (30, 15))
        self.screen.blit(score_text_2, (centered_score_x, 45))
   
    def debug(self, info, y=480, x=60, font_size=50, color="white", bg_color=None):
                
        # Crear una fuente para el texto de depuración.
        font = pygame.font.Font(None, font_size)  # Fuente con el tamaño especificado.
        
        # Renderizar la información de depuración como una superficie de texto.
        debug_surf = font.render(str(info), True, color)
        debug_rect = debug_surf.get_rect(topleft=(x, y))

        # Si se especifica un color de fondo, dibujar el rectángulo de fondo.
        if bg_color:
            pygame.draw.rect(self.screen, bg_color, debug_rect)

        # Dibujar el texto de depuración en la pantalla.
        self.screen.blit(debug_surf, debug_rect)

    def show_fps(self, fps):
        self.fps = fps
        fps_text = self.font.render(f"FPS: {int(self.fps)}", True, (255, 255, 255))  # Blanco
        self.screen.blit(fps_text, (10, 100))  # Posición en la esquina superior izquierda

    # def draw_bezier_path(self, surface):
    # # Número de puntos para la línea de puntos
    #     num_points = 50
    #     curve_colors = [(255, 255, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0)]  # Colores para cada curva
    #     control_colors = [(255, 0, 0), (0, 255, 255), (255, 0, 255), (0, 255, 0)]  # Colores para los puntos de control
    #     radius = 3  # Tamaño de los puntos de control

        
    #     if self.game.formation.attack_mode:
    #         # Número de puntos para la línea de puntos
    #         num_points = 50  # Aumenta o disminuye el número de puntos para ajustar la calidad del dibujo
    #         curve_color = (255, 255, 255)  # Color de la curva
    #         radius = 2  # Tamaño de los puntos de control (opcional)

    #         # Asegurarse de que haya curvas de ataque definidas
    #         if len(self.attack_curves) > 0:
    #             for curve_index, curve in enumerate(self.attack_curves):
    #                 previous_point = None  # Almacena el punto anterior para dibujar líneas entre puntos

    #                 # Dibujar la línea punteada de la curva
    #                 for i in range(num_points + 1):
    #                     t = i / num_points  # Valor de t entre 0 y 1
    #                     point = self.bezier_curve(curve, t)  # Calcular el punto en la curva
    #                     x, y = int(point[0]), int(point[1])  # Convertir las coordenadas a enteros

    #                     # Dibujar un pequeño círculo en cada punto de la curva (para hacerla punteada)
    #                     if previous_point:
    #                         if i % 2 == 0:  # Hacer líneas punteadas (dibujar en cada 2do punto)
    #                             pygame.draw.line(surface, curve_color, previous_point, (x, y), 1)

    #                     previous_point = (x, y)  # Actualizar el punto anterior para la siguiente línea

    #                 # Opcional: dibujar los puntos de control
    #                 for control_point in curve:
    #                     control_x, control_y = int(control_point[0]), int(control_point[1])

    #                     # Dibujar un círculo para el punto de control (opcional)
    #                     pygame.draw.circle(surface, curve_color, (control_x, control_y), radius)

            
        
        
    #     if len(self.game.formation.aliens.curves) > 0:
    #         for curve_index, curve in enumerate(self.curves):
    #             # Escoger el color de la curva y de los puntos de control
    #             curve_color = curve_colors[curve_index % len(curve_colors)]
    #             control_color = control_colors[curve_index % len(control_colors)]

    #             # Dibujar la línea punteada de la curva
    #             for i in range(num_points + 1):
    #                 t = i / num_points  # Valor de t entre 0 y 1
    #                 point = self.bezier_curve(curve, t)  # Calcular el punto en la curva
    #                 x, y = int(point[0]), int(point[1])  # Convertir las coordenadas a enteros

    #                 # Dibujar un círculo en cada punto de la curva
    #                 #pygame.draw.circle(surface, curve_color, (x, y), radius - 1)

    #             # Dibujar los puntos de control con sus coordenadas
    #             for control_point in curve:
    #                 control_x, control_y = int(control_point[0]), int(control_point[1])

    #                 # Dibujar un círculo para el punto de control
    #                 #pygame.draw.circle(surface, control_color, (control_x, control_y), radius + 2)

    #                 # Dibujar el valor (x, y) del punto de control sobre el punto
    #                 text_surface = self.formation.game.FONT.render(f"({control_x}, {control_y})", True, control_color)
    #                 surface.blit(text_surface, (control_x + 5, control_y + 5))  # Colocar el texto cerca del punto de control


           