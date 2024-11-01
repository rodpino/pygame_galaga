import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, sprite_coords, explosion_size, frame_duration=0.05, color_key=(0, 0, 0)):
        super().__init__()
        self.index = 0
        self.frame_duration = frame_duration  # Duración de cada fotograma en segundos
        self.time_accumulator = 0  # Acumulador de tiempo para delta_time
        self.screen = pygame.display.get_surface()
        self.sprite_sheet = sprite_sheet
        self.explosion_size = explosion_size

        # Cargar y escalar todos los sprites en una lista con un bucle
        self.lista_explosion = []
        for coord in sprite_coords:
            sprite = self.sprite_sheet.subsurface(coord)
            sprite = pygame.transform.scale(sprite, self.explosion_size)
            sprite.set_colorkey(color_key)
            self.lista_explosion.append(sprite)

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
