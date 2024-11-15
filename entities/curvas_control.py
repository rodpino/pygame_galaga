import numpy as np


class Curvas_control:
    def __init__(self, game):
        self.game = game
        self.width = self.game.settings.WIDTH

    def control_points_1(self):
        """ superior izquierdo """
        return np.array([
            [188, -10],
            [320, 230],
            [560, 260],
            [580, 450]
        ])

    def control_points_2(self):
        """ superior izquierdo """
        return np.array([
            [580, 450],
            [592, 638],
            [352, 657],
            [342, 463]
        ])

    def control_points_3(self):
        """ loop izquierdo """
        return np.array([
            ([-5, 706]),
            ([205, 659]),
            ([263, 524]),
            ([212, 463])
        ])

    def control_points_4(self):
        """ loop izquierdo """
        return np.array([
            ([212, 463]),
            ([163, 356]),
            ([15, 410]),
            ([56, 517])
        ])

    def control_points_5(self):
        """ loop izquierdo """
        return np.array([
            ([56, 517]),
            ([123, 619]),
            ([248, 561]),
            ([260, 463])
        ])

    def control_points_6(self):
        """ loop derecho """
        return np.array([
            ([self.width + 5, 706]),
            ([self.width - 205, 659]),
            ([self.width - 263, 524]),
            ([self.width - 212, 463])
        ])

    def control_points_7(self):
        """ loop derecho """
        return np.array([
            ([self.width - 212, 463]),
            ([self.width - 163, 356]),
            ([self.width - 15, 410]),
            ([self.width - 56, 517])
        ])

    def control_points_8(self):
        """ loop derecho """
        return np.array([
            ([self.width - 56, 517]),
            ([self.width - 123, 619]),
            ([self.width - 248, 561]),
            ([self.width - 260, 463])
        ])

    def control_points_10(self):
        """ superior oblicuo izquierdo """
        return np.array([
            [250, -10],
            [320, 250],
            [560, 195],
            [580, 385]
        ])

    def control_points_11(self):
        """ superior oblicuo izquierdo """
        return np.array([
            [580, 385],
            [590, 650],
            [280, 680],
            [330, 415]
        ])

    def control_points_12(self):
        """ superior derecho """
        return np.array([
            [self.width - 188, -10],
            [self.width - 320, 230],
            [self.width - 560, 260],
            [self.width - 580, 450]
        ])

    def control_points_13(self):
        """ superior derecho """
        return np.array([
            [self.width - 580, 450],
            [self.width - 592, 638],
            [self.width - 352, 657],
            [self.width - 342, 463]
        ])

    def control_points_14(self):
        """ superior oblicuo derecho """
        return np.array([
            [self.width - 250, -10],
            [self.width - 320, 250],
            [self.width - 560, 195],
            [self.width - 580, 385]
        ])

    def control_points_15(self):
        """ superior oblicuo derecho """
        return np.array([
            [self.width - 580, 385],
            [self.width - 650, 650],
            [self.width - 280, 680],
            [self.width - 300, 415]
        ])
