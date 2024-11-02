import pygame
pygame.init ()

font = pygame.font.Font("asset/fonts/emulogic.ttf", 8)

def debug (info, y = 180, x = 20):
    screen = pygame.display.get_surface ()
    debug_surf = font.render(str(info), True, "white")
    debug_rect = debug_surf.get_rect (topleft = (x, y))
    #pygame.draw.rect(screen, "black", debug_rect)
    screen.blit (debug_surf, debug_rect)
    
    
def debug_2(self, surface):
        if self.alien_type == 'boss_green':
            # Crear una lista con los nombres y valores de las variables
            debug_info = [
                #f"attack_t: {self.attack_t:.2f}",
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