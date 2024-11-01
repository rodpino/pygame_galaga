
# capture_player.py
import numpy as np
import random

class Curvas_relativas:
    def __init__(self, alien, formation):
        self.alien = alien
        self.formation = formation
        self.attack_curves = []
        self.performing_capture = False
        self.capture_start_time = None
        self.WINDOW_WIDTH = 650
        self.WINDOW_HEIGHT = 950
        
         
    def define_attack_curves_relative(self, offset_x=-50, offset_y=0):
    # Curva base en coordenadas relativas
        random_x = random.randint(50, 170)
        player_x = self.formation.game.player_sprite.rect.centerx  # Obtener la posición en X del jugador
        relative_player_x = player_x - self.alien.x
        width = self.formation.game.WINDOW_WIDTH
        base_curve_1 = np.array([
            [0, 0],  # Comienza desde la posición actual
            [-214, 270],  # Punto intermedio ajustado
            [-28, 456],  # Otro punto ajustado
            [100, 331]   # Final en una posición aleatoria
        ])
        
        base_curve_2 = np.array([
            [100, 331] , 
            [180, 181],
            [-70, 100],
            [-92, 264]  # Final en una posición aleatoria
        ])
        
        base_curve_3 = np.array([
            [-92, 264],
            [-60, 438],  # Un ejemplo de punto intermedio
            [291, 570],  # Otro punto
            [relative_player_x, 1000]  # Final en una posición aleatoria
        ])
        
        
        base_curve_4 = np.array([
            [20, -230],
            [16, -190],  # Un ejemplo de punto intermedio
            [8, -105],  # Otro punto
            [ 0, 0]  # Final en una posición aleatoria
        ])
        

        # Aplicar desplazamientos relativos a los puntos de control
        adjusted_curve_1 = [point + np.array([offset_x, 0]) for point in base_curve_1]
        adjusted_curve_2 = [point + np.array([offset_x, 0]) for point in base_curve_2]  
        adjusted_curve_3 = [point + np.array([offset_x, 0]) for point in base_curve_3]
        adjusted_curve_4 = [point + np.array([offset_x, 0]) for point in base_curve_4]

        # Trasladar la curva al punto inicial del alienígena
        starting_point = np.array([self.alien.x, self.alien.y])
        self.alien.attack_curves = [
        [starting_point + point for point in adjusted_curve_1],
        [starting_point + point for point in adjusted_curve_2],
        [starting_point + point for point in adjusted_curve_3],
        [starting_point + point for point in adjusted_curve_4]
    ]

        # Agregar más segmentos si es necesario (por ejemplo, retorno al grid)
        # Aquí puedes definir más curvas de ataque ajustadas


    
    def define_attack_curves_relative_2(self, offset_x=0, offset_y=0):
    # Curva base en coordenadas relativas
        random_x = random.randint(-150, -70)
        player_x = self.formation.game.player_sprite.rect.centerx  # Obtener la posición en X del jugador
        relative_player_x = player_x - self.alien.x
        width = self.formation.game.WINDOW_WIDTH
        base_curve_1 = np.array([
            [0, 0],  # Comienza desde la posición actual
            [214, 270],  # Punto intermedio ajustado
            [28, 456],  # Otro punto ajustado
            [-100, 331]   # Final en una posición aleatoria
        ])
        
        base_curve_2 = np.array([
            [-100, 331] , 
            [-180, 181],
            [70, 100],
            [92, 264]  # Final en una posición aleatoria
        ])
        
        base_curve_3 = np.array([
            [92, 264],
            [60, 438],  # Un ejemplo de punto intermedio
            [-291, 570],  # Otro punto
            [relative_player_x, 1000]  # Final en una posición aleatoria
        ])
        
        
        base_curve_4 = np.array([
            [-20, -230],
            [-16, -190],  # Un ejemplo de punto intermedio
            [-8, -105],  # Otro punto
            [ 0, 0]  # Final en una posición aleatoria
        ])
        

        # Aplicar desplazamientos relativos a los puntos de control
        adjusted_curve_1 = [point + np.array([offset_x, 0]) for point in base_curve_1]
        adjusted_curve_2 = [point + np.array([offset_x, 0]) for point in base_curve_2]  
        adjusted_curve_3 = [point + np.array([offset_x, 0]) for point in base_curve_3]
        adjusted_curve_4 = [point + np.array([offset_x, 0]) for point in base_curve_4]

        # Trasladar la curva al punto inicial del alienígena
        starting_point = np.array([self.alien.x, self.alien.y])
        self.alien.attack_curves = [
        [starting_point + point for point in adjusted_curve_1],
        [starting_point + point for point in adjusted_curve_2],
        [starting_point + point for point in adjusted_curve_3],
        [starting_point + point for point in adjusted_curve_4]
    ]

        # Agregar más segmentos si es necesario (por ejemplo, retorno al grid)
        # Aquí puedes definir más curvas de ataque ajustadas
