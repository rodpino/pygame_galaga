import pygame
import random

class Background:
    def __init__(self, game ):
        self.game = game
        self.screen = pygame.display.get_surface()
        self.scroll_speed = 0.5
        self.toggle_interval = 40
        self.toggle_timer = 0
        self.show_first_half = True
        self.background_y = 0
        
        self.colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (128, 128, 128)]  # rojo, azul, amarillo, gris
        self.rects = self.generate_rects(80)
        self.first_half, self.second_half = self.split_rects()

    def generate_rects(self, num_rects):
        rects = []
        for _ in range(num_rects):
            x = random.randint(0, self.game.WINDOW_WIDTH - 4)
            y = random.randint(0, self.game.WINDOW_HEIGHT - 4)
            color = random.choice(self.colors)
            rects.append((pygame.Rect(x, y, 2, 1), color))
        return rects

    def split_rects(self):
        half_index = len(self.rects) // 2
        return self.rects[:half_index], self.rects[half_index:]

    def update(self, delta_time):
        self.background_y += self.scroll_speed
        if self.background_y >= self.game.WINDOW_HEIGHT:
            self.background_y = 0

        self.toggle_timer += delta_time * 200
        if self.toggle_timer >= self.toggle_interval:
            self.show_first_half = not self.show_first_half
            self.toggle_timer = 0

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fondo negro

        if self.show_first_half:
            for rect, color in self.first_half:
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y - self.game.WINDOW_HEIGHT))
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y))
        else:
            for rect, color in self.second_half:
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y - self.game.WINDOW_HEIGHT))
                self.screen.blit(self.draw_rect(rect, color), (rect.x, rect.y + self.background_y))

    def draw_rect(self, rect, color):
        surface = pygame.Surface((rect.width, rect.height))
        surface.fill(color)
        return surface
