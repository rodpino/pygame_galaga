# capture_player.py
import numpy as np
import random


class CapturePlayer:
    def __init__(self, alien, game):
        self.alien = alien
        self.game = game
        self.attack_curves = []
        self.performing_capture = False
        self.capture_start_time = None
       

    def define_capture_curves_1(self, offset_x=0):
        random_x = random.randint(-80, 80)
        self.attack_curves = [
            self.capture_control_points_1(random_x, offset_x),
            self.capture_control_points_2(random_x, offset_x),
            self.capture_control_points_3(offset_x)
        ]
        # Asignar las curvas de ataque al alienígena
        self.alien.attack_curves = self.attack_curves
        self.alien.curve_attack_index = 0  # Reiniciar el índice de la curva
        self.alien.attack_t = 0.0  # Reiniciar el parámetro t
        self.performing_capture = True
        self.capture_start_time = None

    def define_capture_curves_2(self, offset_x=0):
        random_x = random.randint(-80, 80)
        self.attack_curves = [
            self.capture_control_points_4(random_x, offset_x),
            self.capture_control_points_5(random_x, offset_x),
            self.capture_control_points_6(offset_x)
        ]
         # Asignar las curvas de ataque al alienígena
        self.alien.attack_curves = self.attack_curves
        self.alien.curve_attack_index = 0  # Reiniciar el índice de la curva
        self.alien.attack_t = 0.0  # Reiniciar el parámetro t
        self.performing_capture = True
        self.capture_start_time = None

    def capture_control_points_1(self, random_x, offset_x=0):
        
        return np.array([
            [self.alien.x, self.alien.y],
            [175 + random_x, 123],
            [97 + random_x, 250],
            [160 + random_x, 680]
        ])
        
    def capture_control_points_2(self, random_x, offset_x=0):
        return np.array([
            [160 + random_x, 680],
            [165 + random_x, 655],
            [180 + random_x, 790],
            [220 + random_x, 1000]
        ])

    def capture_control_points_3(self, offset_x=0):
        return np.array([
            [205, -10],
            [185, 35],
            [215, 90],
            [self.alien.x, self.alien.y]
        ])

    # Define capture_control_points_4, capture_control_points_5, and capture_control_points_6 similarly

    def capture_control_points_4(self, random_x, offset_x=0):
        width = self.game.settings.WIDTH
        return np.array([
            [self.alien.x, self.alien.y],
            [width - 175 + random_x, 123],
            [width - 97 + random_x, 250],
            [width - 160 + random_x, 680]  # Final en una posición aleatoria
        ])

    def capture_control_points_5(self, random_x, offset_x=0):
        width = self.game.settings.WIDTH
            
        return np.array([
            [width - 160 + random_x, 680],
            [width - 165 + random_x, 655],
            [width - 180 + random_x, 790],
            [width - 220 + random_x, 1000]  # Final en una posición aleatoria
            ])

    def capture_control_points_6(self, offset_x=0):
        width = self.game.settings.WIDTH
        random_x = random.randint(135, 145)
        return np.array([
            [width - 205, -10],
            [width - 185, 35],
            [width - 215, 90],
            [self.alien.x, self.alien.y]  # Final en una posición aleatoria
        ])

