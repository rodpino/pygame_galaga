import pygame


class CaptureLight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.capture_animation_frames = [
            self.game.resources.get_sprite((289, 36, 48, 80), self.game.settings.CAPTURE_SIZE),
            self.game.resources.get_sprite((339, 36, 48, 80), self.game.settings.CAPTURE_SIZE),
            self.game.resources.get_sprite((389, 36, 48, 80), self.game.settings.CAPTURE_SIZE)
        ]
        self.image = self.capture_animation_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Variables de animación
        self.is_capturing = False  # Controla si está en proceso de captura
        self.capture_start_time = None  # Tiempo en que comienza la captura
        self.frame_index = 0  # Índice del frame de animación actual

    def start_capture(self):
        """Inicia la animación de captura."""
        if not self.is_capturing:  # Solo inicia si no está ya en captura
            self.is_capturing = True
            self.capture_start_time = pygame.time.get_ticks()

    def update(self, frame_rect):
        """Actualiza la animación y verifica colisiones."""
        # Verificar colisión con el jugador
        #if self.rect.colliderect(self.game.player.rect):
        self.start_capture()

        # Reproducir animación si está en captura
        #if self.is_capturing:
        self.animate_capture(frame_rect)
        
    def animate_capture(self, frame_rect):
        """Maneja la animación de captura."""
        if self.capture_start_time is not None:  # Asegurarse de que capture_start_time esté configurado
            elapsed_time = (pygame.time.get_ticks() - self.capture_start_time) / 1000.0
            
            if elapsed_time < 5:  # Limita la animación a 5 segundos
                # Cambiar de frame cada 500 ms
                self.frame_index = int((elapsed_time * 1000) // 500) % len(self.capture_animation_frames)
                
                self.image = self.capture_animation_frames[self.frame_index]
                
            else:
                # Detener la animación después de 5 segundos
                self.is_capturing = False
                self.capture_start_time = None

        # Actualiza la posición del sprite en la pantalla
        self.rect = frame_rect
        
        self.game.screen.blit(self.image, self.rect)
        