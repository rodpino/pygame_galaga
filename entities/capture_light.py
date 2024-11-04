import pygame

class CaptureLight(pygame.sprite.Sprite):
    animation_frames = []  # Asegúrate de que esta lista esté poblada antes de animar
    global_animation_timer = 0.0
    global_animation_interval = 0.4  # Intervalo entre frames en segundos
    global_animation_index = 0

    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.capture_animation_frames = [
            self.game.resources.get_sprite((289, 36, 48, 80), self.game.settings.CAPTURE_SIZE),
            self.game.resources.get_sprite((339, 36, 48, 80), self.game.settings.CAPTURE_SIZE),
            self.game.resources.get_sprite((389, 36, 48, 80), self.game.settings.CAPTURE_SIZE)
        ]
        self.image = self.capture_animation_frames[1]
        self.rect = self.image.get_rect()
        self.rect.center = (300, 600)
        
        # Actualizar la clase con los frames de animación
        CaptureLight.animation_frames = self.capture_animation_frames
        
        # Variables de animación
        self.is_capturing = True  # Activar la captura desde el inicio
        self.capture_start_time = None  # Tiempo en que comienza la captura
        self.frame_index = 0  # Índice del frame de animación actual

    @classmethod
    def sprite_animation(cls, delta_time):
        cls.global_animation_timer += delta_time
        max_index = len(cls.animation_frames)  # Obtener la longitud de animation_frames
        
        if max_index > 0 and cls.global_animation_timer >= cls.global_animation_interval:
            cls.global_animation_timer -= cls.global_animation_interval
            cls.global_animation_index = (cls.global_animation_index + 1) % max_index

    def update(self, delta_time):
        # Llamar al método de animación de clase para actualizar el índice
        CaptureLight.sprite_animation(delta_time)
        position = self.game.formation.aliens.capture_frame_position
        # Actualizar la imagen del sprite usando el índice global de animación
        frames = self.capture_animation_frames
        if len(frames) > 0:  # Verificar que haya frames disponibles
            self.image = frames[self.global_animation_index]
    
        # Actualiza la posición del sprite en la pantalla
        self.rect = self.image.get_rect(center=position)
        self.image = pygame.image.load("asset/Galaga_SpritesSheet.png")
        
     
        
       

    
        