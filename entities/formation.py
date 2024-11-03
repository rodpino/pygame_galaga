import pygame
import random
from entities.alien import Alien

class Formation:
    def __init__(self, game):
        self.game = game
          
        self.aliens = pygame.sprite.Group()  # Grupo de sprites para los alienígenas
        self.grid_size_x = 20.0
        self.grid_size_y = 35.0

        # Movimiento lateral del grid durante la llegada de los aliens
        self.move_distance = 40  # Distancia total de movimiento lateral del grid
        self.move_speed = 50  # Velocidad de movimiento lateral del grid (píxeles por segundo)
        self.direction = 1  # 1: derecha, -1: izquierda
        self.current_move = 0  # Movimiento lateral acumulado del grid
        self.lateral_movement_active = True  # El movimiento lateral está activo

        # Movimiento lateral después de que los aliens hayan llegado
        self.aliens_arrived = False  # Indica si todos los aliens han llegado

        self.initial_target_positions = []  # Posiciones objetivo iniciales (sin movimiento)
        self.create_formation()

        # Variables para el patrón de expansión continuo
        self.expanding = False
        self.expansion_duration = 2.0  # Duración total de cada ciclo de expansión
        self.expansion_elapsed = 0.0

        # Fases de llegada de alienígenas
        self.current_phase = 0  # Índice de la fase actual

        # Temporizadores para ataques
        self.attack_mode = False
        self.attack_timer = 0.0
        self.attack_interval = random.uniform(1.0, 2.0)
        self.attack_formations = []
        self.define_attack_formations()
        self.allowed_attack_types = ['red', 'blue', 'boss_green', 'boss_green, red, red']
        #self.curvas_relativas = Curvas_relativas (self)
    def create_formation(self):
        """Crear alienígenas y calcular sus posiciones objetivo."""
        self.add_aliens_to_group("red", 16)
        self.add_aliens_to_group("blue", 20, offset=16)
        self.add_aliens_to_group("boss_green", 4, offset=36)

    def add_aliens_to_group(self, alien_type, count, offset=0):
        """Agrega un grupo de alienígenas a la formación."""
        for mIndex in range(count):
            bezier_id = mIndex
            x, y = self.calculate_target_position(mIndex, alien_type)
            self.initial_target_positions.append((x, y))
            alien = Alien(mIndex + offset, self, alien_type, bezier_id, self.game)
            self.aliens.add(alien)

    def calculate_target_position(self, mIndex, alien_type):
        
        if alien_type == "boss_green":
            # Posicionar los 4 alienígenas verdes en una sola fila con simetría alrededor del centro
            row = 2  # Fila específica para los alienígenas verdes (tercera fila, indexada como 2)
            
            # Alternar la posición en X para cada alien en el grupo de 4
            if mIndex == 0 or mIndex == 2:
                # Lado izquierdo
                sign = -1
            else:
                # Lado derecho
                sign = 1

            # Asignar el desplazamiento horizontal basado en el índice
            col = mIndex // 2  # 0 o 1 para cada par de alienígenas en el lado izquierdo y derecho
            retVal_x = (self.grid_size_x + self.grid_size_x * 2 * col) * sign

            # Asignar la posición en Y para la única fila de alienígenas verdes
            retVal_y = (row * self.grid_size_y) + 70
        
        else:
            group = mIndex // 4
            pos_in_group = mIndex % 4

            # Posición en Y
            if pos_in_group == 0 or pos_in_group == 1:
                retVal_y = self.grid_size_y * 0  # Primera fila
            else:
                retVal_y = self.grid_size_y * 1  # Segunda fila

            # Alternar posición en X para cada alien en el grupo
            if pos_in_group == 0 or pos_in_group == 2:
                # Lado izquierdo
                sign = -1
            else:
                # Lado derecho
                sign = 1

            retVal_x = (self.grid_size_x + self.grid_size_x * 2 * group) * sign

            # Ajustar posiciones para la pantalla
            screen_x = retVal_x + self.game.settings.WIDTH // 2
            screen_y = retVal_y + 180  # Posición objetivo en Y
            
            if alien_type == "blue":
                screen_y += 70
            # elif alien_type == "boss_green":
            #     screen_y += 350
            return int(screen_x), int(screen_y)
        
        # Ajustar posiciones para la pantalla para los alienígenas verdes
        screen_x = retVal_x + self.game.settings.WIDTH // 2
        screen_y = retVal_y  # Posición objetivo en Y para los alienígenas verdes

        return int(screen_x), int(screen_y)

    def get_initial_target_position(self, mIndex):
        return self.initial_target_positions[mIndex]

    def get_grid_center(self):
        """Calcula el centro del grid."""
        xs, ys = zip(*self.initial_target_positions)
        center_x = sum(xs) / len(xs)
        center_y = sum(ys) / len(ys)
        return center_x, center_y

    def get_adjusted_index(self, alien):
        if alien.alien_type == "red":
            group = alien.mIndex // 4
        elif alien.alien_type == "blue":
            group = (alien.mIndex - 16) // 4  # Ajuste para los alienígenas azules
        elif alien.alien_type == "boss_green":
            group = (alien.mIndex - 36) // 4
        else:
            group = 0  # Valor por defecto para otros tipos de alienígenas              
            
        adjusted_index = group
        return adjusted_index
    
    def all_aliens_in_final_position(self):
        """Verifica si todos los alienígenas han alcanzado su posición final en el grid."""
        return all(alien.arrived for alien in self.aliens)

    def apply_expansion(self, delta_time):
        #"""Aplica la expansión a todos los aliens en la formación."""
        self.expansion_elapsed += delta_time
        if self.expansion_elapsed >= self.expansion_duration:
            self.expansion_elapsed = 0.0

        progress = self.expansion_elapsed / self.expansion_duration
        expansion_progress = progress / 0.5 if progress < 0.5 else (1 - (progress - 0.5) / 0.5)

        for alien in self.aliens:
            if not alien.attack_mode:
                adjusted_index = self.get_adjusted_index(alien)
                sign = -1 if alien.is_left_alien() else 1
                max_offset = sign * 30 * ((adjusted_index + 1) / 4)

                # Aplicar modificaciones específicas por tipo
                if alien.alien_type == "red" and alien.mIndex in [0, 1, 2, 3]:
                    max_offset *= 0.5
                if alien.alien_type == "blue" and alien.mIndex in [16, 17, 18, 19]:
                    max_offset *= 0.5
                if alien.alien_type == "boss_green" and alien.mIndex in [36, 37]:
                    max_offset *= 0.5
                if alien.alien_type == "boss_green" and alien.mIndex in [38, 39]:
                    max_offset *= 2

                alien.expansion_offset = max_offset * expansion_progress
                alien.expansion_offset_y = 25 * expansion_progress
            else:
                # Si el alien está en modo ataque, restablecer los desplazamientos de expansión
                alien.expansion_offset = 0.0
                alien.expansion_offset_y = 0.0
               # Actualizar movimiento lateral del grid si está activo
        
    def update_arrival_phases(self, delta_time):
        
        # Actualiza las fases de llegada de los alienígenas        
        if self.current_phase == 0:
        # Fase 1: Alienígenas rojos 0-3
            if all(alien.arrived for alien in self.aliens if alien.mIndex in [0, 1, 2, 3]):
                self.current_phase += 1
                self.reset_start_time("blue", [0, 1, 2, 3])
               

        elif self.current_phase == 1:
            # Fase 2: Alienígenas azules 16-19
            if all(alien.arrived for alien in self.aliens if alien.mIndex in [16, 17, 18, 19]):
                self.current_phase += 1
                self.reset_start_time("red", [4, 5, 6, 7])
                self.reset_start_time("boss_green", [0, 1, 2, 3])
                    

        elif self.current_phase == 2:
            # Fase 3: Alienígenas rojos 4-7 y verdes 36-39
            if all(alien.arrived for alien in self.aliens if alien.mIndex in [4, 5, 6, 7, 36, 37, 38, 39]):
                self.current_phase += 1
                self.reset_start_time("red", range(8, 16), )
                

        elif self.current_phase == 3:
            # Fase 4: Alienígenas rojos 8-15
            if all(alien.arrived for alien in self.aliens if alien.mIndex in range(8, 16)):
                self.current_phase += 1
                self.reset_start_time("blue", range(4, 12))
                

        elif self.current_phase == 4:
            # Fase 5: Alienígenas azules 20-27
            if all(alien.arrived for alien in self.aliens if alien.mIndex in range(20, 28)):
                self.current_phase += 1
                self.reset_start_time("blue", range(12, 20))
                

        elif self.current_phase == 5:
            # Fase 6: Alienígenas azules 28-35
            if all(alien.arrived for alien in self.aliens if alien.mIndex in range(28, 36)):
                self.aliens_arrived = True
                # self.moving_to_center = True
                self.lateral_movement_active = False  # Detener el movimiento lateral de inmediato
                self.centering_time_elapsed = 0.0
                self.current_move_start = self.current_move
                self.expanding = True
           
    
    def update_lateral_movement(self, delta_time):
        """Actualiza el movimiento lateral del grid."""
        
        if self.lateral_movement_active:
                self.current_move += self.move_speed * delta_time * self.direction
                if abs(self.current_move) >= self.move_distance:
                    self.current_move = self.move_distance * self.direction
                    self.direction *= -1  # Cambiar dirección
        
    def apply_continuous_expansion(self, delta_time):
        """Aplica la expansión continua al grid."""
        if self.expanding:
            self.apply_expansion(delta_time)
            
    def define_attack_formations(self):
        # Definir las formaciones de ataque
        self.attack_formations = [
            ['red'],
            ['blue'],
            ['boss_green'],
            ['boss_blue'],
            ['boss_green', 'red'],
            ['boss_green', 'red', 'red'],
            ['boss_blue', 'red'],
            ['boss_blue', 'red', 'red']
            # Agrega más formaciones según necesites
        ]    
        # Cuanto mayor sea el peso, mayor será la probabilidad de selección
        self.attack_weights = [5, 1, 2, 2, 1, 1, 1, 1]  # Ajusta los pesos según tu preferencia

    
               
    def update_attack_phases(self, delta_time):
        if self.all_aliens_in_final_position():
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_interval:
                self.attack_timer = 0.0
                self.attack_interval = random.uniform(0.5, 1.0)
                # Seleccionar una formación de ataque al azar
                formation = random.choices(self.attack_formations, weights=self.attack_weights, k=1)[0]
                if formation == ['boss_green', 'red', 'red'] or formation == ['boss_green', 'red'] or formation == ['boss_blue', 'red'] or formation == ['boss_blue', 'red', 'red']:
                    self.initiate_combined_attack_formation(formation)
                elif formation == ['boss_green'] or formation == ['boss_blue']:
                    self.capture_formation(formation)
                elif formation == ['red'] or formation == ['blue']:
                    #self.capture_formation(formation)   
                    self.initiate_attack_formation(formation)
                
                    
 
 
 
    def capture_formation(self, formation):
        # Buscar alienígenas disponibles que coincidan con los tipos en la formación
        possible_aliens = [alien for alien in self.aliens if alien.alien_type in formation and not alien.attack_mode and alien.arrived]

        if not possible_aliens:
            return

        attack_group = []

        for alien_type in formation:
            aliens_of_type = [alien for alien in possible_aliens if alien.alien_type == alien_type]
            if aliens_of_type:
                # Seleccionar un alienígena al azar del tipo especificado
                alien_to_attack = random.choice(aliens_of_type)
                attack_group.append(alien_to_attack)
                possible_aliens.remove(alien_to_attack)
            else:
                # No hay suficientes alienígenas de este tipo
                return

        # Iniciar ataque para el grupo
        for alien in attack_group:
            alien.attack_mode = True
            alien.is_capture_formation = True  # Indicar que es una formación de captura

            if alien.alien_type == 'boss_green' or alien.alien_type == 'boss_blue':
                # Definir curvas de captura específicas para boss_green
                if alien.mIndex % 2 == 0:
                    alien.capture_player.define_capture_curves_1()
                else:
                    alien.capture_player.define_capture_curves_2()
            # elif alien.alien_type == 'red':
            #     # Definir curvas de ataque para red aliens
            #     if alien.mIndex % 2 == 0:
            #         alien.define_attack_curves_1_1()
            #     else:
            #         alien.define_attack_curves_2_1()

 
    def initiate_attack_formation(self, formation):
        # formation es una lista de tipos de alienígenas, por ejemplo ['boss_green', 'red', 'red']
        possible_aliens = [alien for alien in self.aliens if alien.alien_type in formation and not alien.attack_mode and alien.arrived]
        
        if not possible_aliens:
            return  # No hay alienígenas disponibles para esta formación

        attack_group = []

        for alien_type in formation:
            # Encontrar los alienígenas de este tipo más alejados del jugador
            aliens_of_type = [alien for alien in possible_aliens if alien.alien_type == alien_type]
            if aliens_of_type:
                player_x, player_y = self.game.player.rect.center
                # Ordenar los alienígenas por distancia al jugador (de mayor a menor)
                aliens_of_type.sort(key=lambda alien: ((alien.x - player_x)**2 + (alien.y - player_y)**2), reverse=True)
                # Seleccionar los dos más alejados, o menos si no hay suficientes
                farthest_aliens = aliens_of_type[:3]
                if farthest_aliens:
                # Elegir uno de los dos de forma aleatoria para atacar
                    alien_to_attack = random.choice(farthest_aliens)
                    attack_group.append(alien_to_attack)
                    possible_aliens.remove(alien_to_attack)
            else:
                # No hay suficientes alienígenas disponibles de este tipo
                return

        # Iniciar ataque para el grupo
        for alien in attack_group:
            alien.attack_mode = True
            alien.is_capture_formation = False  # No es una formación de captura
            # Aplicar la curva según si el índice del alien es par o impar
            if alien.mIndex % 2 == 0:  # Si el índice es par
                alien.define_attack_curves_2()
                
            else:  # Si el índice es impar
                #alien.define_attack_curves_3()
                self.initiate_red_attack_group_1()
                
                
    def initiate_combined_attack_formation(self, formation):
        # Obtener los índices de las formaciones específicas
        formations_indices = [
            [38, 8, 4],
            [36, 4, 0],
            [37, 1, 5],
            [39, 5, 9]
        ]

        possible_aliens = [alien for alien in self.aliens if not alien.attack_mode and alien.arrived]

        if not possible_aliens:
            return

        player_x, player_y = self.game.player.rect.center
        farthest_group = None
        farthest_distance = -float('inf')

        for indices in formations_indices:
            aliens_in_formation = [alien for alien in possible_aliens if alien.mIndex in indices]

            # Verificar que los alienígenas en la formación coincidan con el tipo especificado
            formation_types = [alien.alien_type for alien in aliens_in_formation]
            if sorted(formation_types) == sorted(formation):
                # Calcular la distancia promedio al jugador
                avg_distance = sum(
                    ((alien.x - player_x) ** 2 + (alien.y - player_y) ** 2) ** 0.5
                    for alien in aliens_in_formation
                ) / len(aliens_in_formation)

                if avg_distance > farthest_distance:
                    farthest_group = aliens_in_formation
                    farthest_distance = avg_distance

        if farthest_group:
            # Calcular el centro del grupo
            group_center_x = sum(alien.x for alien in farthest_group) / len(farthest_group)
            group_center_y = sum(alien.y for alien in farthest_group) / len(farthest_group)

            # Preparar a cada alienígena en el grupo
            for alien in farthest_group:
                # Restablecer los desplazamientos de expansión
                alien.expansion_offset = 0.0
                alien.expansion_offset_y = 0.0

                # Establecer la posición del alienígena en su posición objetivo inicial
                alien.x = alien.initial_target_x
                alien.y = alien.initial_target_y

                alien.attack_mode = True
                alien.is_capture_formation = False  # No es una formación de captura

                # Calcular el desplazamiento relativo en X e Y para cada alienígena
                relative_offset_x = alien.initial_target_x - group_center_x
                relative_offset_y = alien.initial_target_y - group_center_y

                # Asignar la curva adecuada según si el alienígena es par o impar
                if alien.mIndex % 2 == 0:
                    # Alienígenas pares usan define_attack_curves_relative
                    alien.curvas_relativas.define_attack_curves_relative(relative_offset_x, relative_offset_y)
                else:
                    # Alienígenas impares usan define_attack_curves_relative_2
                    alien.curvas_relativas.define_attack_curves_relative_2(relative_offset_x, relative_offset_y)


                            
                    
    def initiate_red_attack_group_1(self):
        """Inicia el ataque para el grupo 1 de alienígenas rojos."""
        red_aliens_group_1 = [alien for alien in self.aliens]
        if red_aliens_group_1:
            attacking_alien = random.choice(red_aliens_group_1)
            attacking_alien.attack_mode = True
            attacking_alien.define_attack_curves()
    
    def initiate_boss_green_attack_group_1(self):
        """Inicia el ataque para el grupo 1 de alienígenas rojos."""
        boss_green_aliens_group_1 = [alien for alien in self.aliens if alien.mIndex in [36, 39]]
        if boss_green_aliens_group_1:
            attacking_alien = random.choice(boss_green_aliens_group_1)
            attacking_alien.attack_mode = True
            attacking_alien.define_attack_curves_2()   
            
                
            
        
            
    def apply_lateral_movement_to_aliens(self):
        """Aplica el movimiento lateral del grid a cada alienígena."""
        if not self.expanding:
            for alien in self.aliens:
                alien.grid_offset_x = self.current_move        
                        

    def reset_start_time(self, alien_type, bezier_id):
        """Reinicia el tiempo de inicio para los alienígenas especificados."""
        for alien in self.aliens:
            if alien.alien_type == alien_type and alien.bezier_id in bezier_id:
                alien.time_since_start = 0.0

    def draw(self, surface):
        for alien in self.aliens:
            alien.draw(surface)
            
        
    
    def update(self, delta_time):
        
        # Actualizar movimiento lateral
        self.update_lateral_movement(delta_time)
        
        # Actualizar fases de llegada
        self.update_arrival_phases(delta_time)
        
        # Aplicar expansión continua
        self.apply_continuous_expansion(delta_time)
        
        self.apply_lateral_movement_to_aliens()
        
        # Actualizar fases de ataque
        self.update_attack_phases(delta_time)
        
        # # Actualizar la lógica de cada alienígena
        self.aliens.update(delta_time)
        