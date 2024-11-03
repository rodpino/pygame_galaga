import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.index = 0
        self.frame_duration = 0.05  # Duración de cada fotograma en segundos
        self.time_accumulator = 0  # Acumulador de tiempo para delta_time
        self.screen = pygame.display.get_surface()
        self.explosion_size = (70, 70)

        sprite_coordinates = [
                                (289, 1, 32, 32),
                                (323, 1, 32, 32),
                                (357, 1, 32, 32),
                                (399, 1, 32, 32),
                                (425, 1, 32, 32)
                            ]

    # Usamos una comprensión de lista para llamar a get_sprite con cada coordenada
        self.lista_explosion = [
            self.game.resources.get_sprite(coord, self.explosion_size) for coord in sprite_coordinates
            ]


        
        self.image = self.lista_explosion[self.index]
        self.rect = self.image.get_rect()
        self.active = False  # Añadir estado activo para controlar la animación
        self.finished = False  # Indica si la animación ha terminado

    def update(self, delta_time, pos=None):
        if self.active:  # Solo actualizar si está activo
            if pos:
                self.rect.center = pos
            self.time_accumulator += delta_time

            # Cambiar el fotograma cuando se acumule suficiente tiempo
            if self.time_accumulator >= self.frame_duration:
                self.time_accumulator -= self.frame_duration
                self.explosion_index()

            # Solo dibujar la imagen si la animación sigue activa
            if self.active:
                self.image = self.lista_explosion[self.index]
                

    def explosion_index(self):
        self.index += 1
        if self.index >= len(self.lista_explosion):
            self.index = 0
            self.active = False  # Detener la animación al final
            self.finished = True  # Marcar que la animación ha terminado
            self.kill() 
    def start_explosion(self, pos):
        self.active = True  # Activar la animación
        self.finished = False  # Reiniciar el estado terminado
        self.index = 0
        self.time_accumulator = 0  # Reiniciar el acumulador de tiempo
        self.rect.center = pos

    def is_finished(self):
        return self.finished
