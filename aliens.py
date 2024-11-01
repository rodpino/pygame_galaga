import pygame
import math
import random
import numpy as np
from setting import *
from explosion import *
from pygame.locals import *
from debug import *
from alien_laser import *
from grid import *


class Aliens(pygame.sprite.Sprite):
    
    global_animation_index = 0  # Variable global para la sincronización de animación
    global_velocity_move = 0
    
    def __init__(self):
        super().__init__()
        
        self.screen = pygame.display.get_surface()
        self.sprite_sheet = pygame.image.load("asset/Galaga_SpritesSheet.png").convert_alpha()
        self._load_sprites()
        self._group_sprites()
        self.index = 0
        self.velocity_move = 1
        self.cambiar = True
        #self.alien_blue = [self.alien_azul_1, self.alien_azul_2]
        self.original_image = self.sprites[0]
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)   

        self.laser_group = pygame.sprite.Group()
        self.shoot_cooldown = 200  # Tiempo de enfriamiento entre disparos
        self.last_shot_time = 0
        
    def _load_sprites(self):
        sprite_coords = [
            (109, 37, SPRITE_SIZE, SPRITE_SIZE), (127, 37, SPRITE_SIZE, SPRITE_SIZE),
            (109, 55, SPRITE_SIZE, SPRITE_SIZE), (127, 55, SPRITE_SIZE, SPRITE_SIZE),
            (109, 73, SPRITE_SIZE, SPRITE_SIZE), (127, 73, SPRITE_SIZE, SPRITE_SIZE),
            (109, 91, SPRITE_SIZE, SPRITE_SIZE), (127, 91, SPRITE_SIZE, SPRITE_SIZE)
        ]

        self.sprites = [pygame.transform.scale(self.sprite_sheet.subsurface(coords), ALIENS_SIZE) for coords in sprite_coords]
        for sprite in self.sprites:
            sprite.set_colorkey((0, 0, 0))

        self.alien_verde_1, self.alien_verde_2, self.alien_azul_1, self.alien_azul_2, \
        self.alien_butterfly_red_1, self.alien_butterfly_red_2, \
        self.alien_butterfly_blue_1, self.alien_butterfly_blue_2 = self.sprites

    def _group_sprites(self):
        self.alien_green = [self.alien_verde_1, self.alien_verde_2]
        self.alien_blue = [self.alien_azul_1, self.alien_azul_2]
        self.alien_butterfly_red = [self.alien_butterfly_red_1, self.alien_butterfly_red_2]
        self.alien_butterfly_blue = [self.alien_butterfly_blue_1, self.alien_butterfly_blue_2]

    def cambiar_sprite(self):
        self.cambiar = True
        
    def change_to_blue(self):
        self.original_image = self.alien_blue[0]
        self.image = self.original_image.copy()
        self.mask = pygame.mask.from_surface(self.image)  # Actualizar la máscara con la nueva imagen    
        
    
    def move_aliens(self):
       
        offset = 0.1
        separation_factor = 1  # Ajusta este factor para aumentar la separación
        self.t = (self.step / self.num_steps) * separation_factor + offset
        self.t = min(self.t, 1.0)  # Asegura que t no sea mayor a 1.0
    
        
        # self.t = self.step / self.num_steps
        self.new_position = self.bezier_curve(self.t)
        self.velocity = self.new_position - self.position
        self.position = self.new_position
        self.rect.center = (int(self.position[0]), int(self.position[1]))
        self.angle = np.degrees(np.arctan2(-self.velocity[1], self.velocity[0]))
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.step += 1
        self.last_position = self.position.copy()
        self.step += self.speed_factor  
        #self.update_animation() 
    def bezier_curve(self, t):
        P0, P1, P2, P3 = self.points
        return (1-t)**3 * np.array(P0) + 3*(1-t)**2 * t * np.array(P1) + 3*(1-t) * t**2 * np.array(P2) + t**3 * np.array(P3)

    def move_towards_target(self, speed=4):
        target_x, target_y = self.target
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * speed
        self.rect.y += dy * speed
        self.update_animation ()
        if distance != 0:
            self.angle = np.degrees(np.arctan2(-dy, dx))

            self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)

        if abs(self.rect.x - target_x) < speed and abs(self.rect.y - target_y) < speed:
            self.rect.x = target_x
            self.rect.y = target_y
            self.moving = False
            self.phase = 6
              
            self.image = pygame.transform.rotate(self.original_image, 0)
            #self.rect = self.image.get_rect(center=self.rect.center)
            
            return True
        return False
   
        
    @classmethod
    def animar_los_bichos(cls):
        cls.global_velocity_move += 1
        if cls.global_velocity_move >= 2500:
            cls.global_velocity_move = 1
            cls.global_animation_index += 1
            if cls.global_animation_index >= 2:
                cls.global_animation_index = 0
        
        return cls.global_animation_index

    def update_animation(self):
        self.index = Aliens.animar_los_bichos()
        
        
        self.image = self.original_image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        
        
            
    def update(self, dt):
        self.update_animation()
        self.shoot(dt)
        if self.phase == 6 and self.group_id == 1:
            debug(f"Alien {self.alien_id} from group {self.group_id} reached phase 6")
    def shoot(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.last_shot_time = current_time
            if random.random() < 0.1:  # Probabilidad de disparo
                # Pasar la posición del jugador al láser
                player_position = self.game.player_sprite.rect.center
                
                # Decidir si disparo es preciso o con variación
                if random.random() < 0.5:  # 50% de disparos precisos
                    laser = AlienLaser(self.rect.center, player_position, error_margin=0)
                else:  # 50% de disparos con variación
                    laser = AlienLaser(self.rect.center, player_position, error_margin=75)
                
                self.laser_group.add(laser)

class AlienAzul(Aliens):
    def __init__(self, game, grid, position, target_pos, row, col, t_offset=0, group_id=0, speed_factor=1, alien_id=1):
        super().__init__()
        self.speed_factor = speed_factor
        self.game = game
        self.grid = grid
        self.alien_id = alien_id
        self.alien_blue = [self.alien_azul_1, self.alien_azul_2]
        self.original_image = self.alien_butterfly_blue[self.index]
        self.group_id = group_id
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.t = t_offset / 100.0
        self.step = t_offset
        self.hit_count = 0
        self.num_steps = 200
        self.points = self.control_points()
        self.position = np.array(self.points[0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.angle = 0
        self.phase = 1
        self.moving = False
        self.target = target_pos
        self.last_position = self.position.copy()
        
        self.mask = pygame.mask.from_surface(self.image)
        self.target_x, self.target_y = self.grid.get_cell_center(row, col)
        
    def control_points(self):
        return np.array([WIDTH / 2 + 20, -10]), np.array([WIDTH / 2 + 10, 260]), np.array([10, 305]), np.array([65, 470])

    def control_points_2(self):
        return np.array([65, 470]), np.array([98, 543]), np.array([WIDTH / 2 + 10, 480]), np.array([WIDTH / 2 + 5, 400])

    def control_points_3(self):
        return np.array([WIDTH / 2 - 20, -10]), np.array([WIDTH / 2 - 10, 260]), np.array([WIDTH - 10, 305]), np.array([WIDTH - 65, 470])

    def control_points_4(self):
        return np.array([WIDTH - 65, 470]), np.array([WIDTH - 98, 543]), np.array([WIDTH / 2 + 10, 480]), np.array([WIDTH / 2 - 5, 400])
    
    def update(self, dt):
        self.update_animation()
        self.original_image = self.alien_butterfly_blue[self.index]
        
        self.image = self.original_image.copy()
        self.execute_phases()
        
        self.mask = pygame.mask.from_surface(self.image)
        if self.moving:
            self.move_towards_target()
            
        else:
            self.rect.x += self.game.grid.direction * self.game.grid.move_speed    
        # else:
        #     # Ajustar la posición de los alienígenas con el movimiento lateral del grid
        #     self.rect.x += self.game.grid.direction * self.game.grid.move_speed
            
    def execute_phases(self):
        if self.game.current_group in [1, 2] and self.group_id in [1, 2]:
            self.execute_phases_group_1_2()   
        elif self.game.current_group == 6 and self.group_id == 6:
            self.execute_phases_group_6()
        elif self.game.current_group == 7 and self.group_id == 7:
            self.execute_phases_group_7()
        
        
    def execute_phases_group_1_2 (self):
        if self.phase == 1:
            self.points = self.control_points()
            self.move_aliens()
            if self.t >= 1:
                self.phase = 2
                self.step = 0

        elif self.phase == 2:
            self.points = self.control_points_2()
            self.move_aliens()
            if self.t >= 1:
                self.phase = 3
                self.moving = True
                self.step = 0
                self.last_position = self.position.copy()

        elif self.phase == 3:
            if self.move_towards_target():
                self.phase = 6
                self.step = 0
              
    
    def execute_phases_group_6 (self):            
        if self.game.current_group ==6:     
            if self.phase == 1:
                
                self.points = self.control_points_3()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 2
                    self.step = 0

            elif self.phase == 2:
                self.points = self.control_points_4()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 3
                    self.moving = True
                    self.step = 0
                    self.last_position = self.position.copy()

            elif self.phase == 3:
                if self.move_towards_target():
                    self.phase = 6            
    
    
    def execute_phases_group_7 (self):    
        
        
        if self.game.current_group ==7:
           
            if self.phase == 1:
                
                self.points = self.control_points()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 2
                    self.step = 0

            elif self.phase == 2:
                self.points = self.control_points_2()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 3
                    self.moving = True
                    self.step = 0
                    self.last_position = self.position.copy()

            elif self.phase == 3:
                if self.move_towards_target():
                    self.phase = 6       
    

class AlienRojo(Aliens):
    def __init__(self, game, grid, position, target_pos, row, col, t_offset=0, group_id=0, speed_factor=1, alien_id=1):
        super().__init__()
        self.speed_factor = speed_factor
        self.game = game
        self.grid = grid
        self.alien_id = alien_id
        self.original_image = self.alien_butterfly_red[self.index]
        self.group_id = group_id
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.t = t_offset / 100.0
        self.step = t_offset
        self.hit_count = 0
        self.points = self.control_points()
        self.num_steps = 200
        self.position = np.array(self.points[0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.angle = 0
        self.phase = 1
        self.moving = False
        self.target = target_pos
        self.alien_blue = [self.alien_azul_1, self.alien_azul_2]
        
        self.target_x, self.target_y = self.grid.get_cell_center(row, col)
        
    def control_points(self):
        return np.array([WIDTH / 2 - 20, -10]), np.array([WIDTH / 2 - 10, 260]), np.array([WIDTH - 10, 305]), np.array([WIDTH - 65, 470])

    def control_points_2(self):
        return np.array([WIDTH - 65, 470]), np.array([WIDTH - 98, 543]), np.array([WIDTH / 2 + 10, 480]), np.array([WIDTH / 2 - 10, 330])

    def control_points_3(self):
        return np.array([-5, 706]), np.array([205, 659]), np.array([263, 524]), np.array([212, 463])

    def control_points_4(self):
        return np.array([212, 463]), np.array([163, 356]), np.array([15, 410]), np.array([56, 517])

    def control_points_5(self):
        return np.array([56, 517]), np.array([123, 619]), np.array([248, 561]), np.array([212, 463])

    def control_points_6(self):
        return np.array([WIDTH + 5, 706]), np.array([WIDTH - 205, 659]), np.array([WIDTH - 263, 524]), np.array([WIDTH - 212, 463])

    def control_points_7(self):
        return np.array([WIDTH - 212, 463]), np.array([WIDTH - 163, 356]), np.array([WIDTH - 15, 410]), np.array([WIDTH - 56, 517])

    def control_points_8(self):
        return np.array([WIDTH - 56, 517]), np.array([WIDTH - 123, 619]), np.array([WIDTH - 248, 561]), np.array([WIDTH - 212, 463])



 
        
    def update(self, dt):
        self.update_animation()
        self.original_image = self.alien_butterfly_red[self.index]
        self.image = self.original_image.copy()
        self.mask = pygame.mask.from_surface(self.image)  # Actualizar la máscara con la nueva imagen
        
        if self.moving:
            self.move_towards_target()
        else:
            self.rect.x += self.game.grid.direction * self.game.grid.move_speed    
        # else:
        #     # Ajustar la posición de los alienígenas con el movimiento  del grid
        #     self.rect.x += self.game.grid.direction * self.game.grid.move_speed
        
        if self.game.current_group in [1, 2] and self.group_id in [1, 2]:
            self.execute_phases_group_1_2()
        elif self.game.current_group in [3, 4] and self.group_id in [3, 4]:
            self.execute_phases_group_3_4()
        elif self.game.current_group == 5 and self.group_id == 5:
            self.execute_phases_group_5()



        
    def execute_phases_group_1_2(self):
        if self.group_id in [1, 2]:
            if self.phase == 1:
                self.points = self.control_points()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 2
                    self.step = 0
                
            elif self.phase == 2:
                self.points = self.control_points_2()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 3
                    self.step = 0
                    self.last_position = self.position.copy()
                    
            elif self.phase == 3:
                if self.move_towards_target():
                    self.phase = 6
                    print ("CTM estamos fase 6")
                      

    def execute_phases_group_3_4(self):
        if self.group_id in [3, 4]:
            if self.phase == 1:
                self.num_steps = 130
                self.points = self.control_points_3()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 2
                    self.step = 0

            elif self.phase == 2:
                self.num_steps = 130
                self.points = self.control_points_4()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 3
                    self.moving = True
                    self.step = 0

            elif self.phase == 3:
                self.num_steps = 130
                self.points = self.control_points_5()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 4
                    self.moving = True
                    self.step = 0

            elif self.phase == 4:
                if self.move_towards_target():
                    self.phase = 6
                    
                    
    def execute_phases_group_5(self):
        if self.group_id == 5:
            if self.phase == 1:
                self.num_steps = 130
                self.points = self.control_points_6()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 2
                    self.step = 0

            elif self.phase == 2:
                self.num_steps = 130
                self.points = self.control_points_7()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 3
                    self.moving = True
                    self.step = 0

            elif self.phase == 3:
                self.num_steps = 130
                self.points = self.control_points_8()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 4
                    self.moving = True
                    self.step = 0

            elif self.phase == 4:
                if self.move_towards_target():
                    self.phase = 6
                    self.game.current_group == 1                  
                    
                    
                    
                    

class AlienGreen (Aliens):
    def __init__(self, game, grid, position, target_pos, row, col, t_offset=0, group_id=0, speed_factor=1, alien_id=1):
        super().__init__()
        self.alien_blue = [self.alien_azul_1, self.alien_azul_2]
        self.speed_factor = speed_factor
        self.game = game
        self.grid = grid
        self.alien_id = alien_id
        self.original_image = self.alien_green[self.index]
        self.group_id = group_id
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.t = t_offset / 100.0 
        self.step = t_offset
        self.hit_count = 0
        self.points = self.control_points()
        self.num_steps = 200
        self.position = np.array(self.points[0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.angle = 0
        self.phase = 1
        self.moving = False
        self.grid = grid
        self.row = row
        self.target = target_pos
        self.col = col
        self.mask = pygame.mask.from_surface(self.image)  # Crear la máscara inicial
        self.target_x, self.target_y = self.grid.get_cell_center(row, col)
    
    def control_points(self):
        return np.array([-5, 706]), np.array([205, 659]), np.array([263, 524]), np.array([212, 463])
    def control_points_2(self):
        return np.array([212, 463]), np.array([163, 356]), np.array([15, 410]), np.array([56, 517])
    def control_points_3(self):
        return np.array([56, 517]), np.array([123, 619]), np.array([248, 561]), np.array([212, 463])
    
    
    def update(self, dt):
        super().update(dt)
        self.update_animation()
        self.original_image = self.alien_green[self.index]
        if self.hit_count == 1:
            self.original_image = self.alien_blue[self.index]
        self.image = self.original_image.copy()
        self.mask = pygame.mask.from_surface(self.image)
        
        if self.moving:
            self.move_towards_target()
        else:
            self.rect.x += self.game.grid.direction * self.game.grid.move_speed
        #     # Ajustar la posición de los alienígenas con el movimiento lateral del grid
        #     self.rect.x += self.game.grid.direction * self.game.grid.move_speed
            
        if self.game.current_group in [3, 4] and self.group_id in [3, 4]:
            self.execute_phases_group_3_4()
   

    def execute_phases_group_3_4(self):
        if self.group_id == 4:
            if self.phase == 1:
                self.num_steps = 130
                self.points = self.control_points()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 2
                    self.step = 0

            elif self.phase == 2:
                self.num_steps = 130
                self.points = self.control_points_2()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 3
                    self.moving = True
                    self.step = 0

            elif self.phase == 3:
                self.num_steps = 130
                self.points = self.control_points_3()
                self.move_aliens()
                if self.t >= 1:
                    self.phase = 4
                    self.moving = True
                    self.step = 0

            elif self.phase == 4:
                if self.move_towards_target():
                    self.phase = 6