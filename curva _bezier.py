import pygame
import numpy as np
import json
import os

# Configuración inicial
pygame.init()
pygame.display.set_caption('Curvas Bézier Editables con Tablas')
WINDOW_SIZE = (650, 950)
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Archivo donde guardaremos las coordenadas
SAVE_FILE = 'bezier_control_points.json'

# Fuente para texto
font = pygame.font.SysFont('Arial', 24)

# Clase para las curvas Bézier
class BezierCurve:
    def __init__(self, control_points, color):
        self.control_points = control_points
        self.color = color
        self.selected_point = None

    def draw(self, screen):
        # Dibujar la curva Bézier
        num_points = 100
        for i in range(num_points):
            t = i / num_points
            point = self.bezier_curve(self.control_points, t)
            next_point = self.bezier_curve(self.control_points, t + 1 / num_points)
            pygame.draw.line(screen, self.color, point, next_point, 2)

        # Dibujar los puntos de control
        for point in self.control_points:
            pygame.draw.circle(screen, self.color, point, 8)

    def bezier_curve(self, points, t):
        # Calcular la curva Bézier con 4 puntos de control
        return (
            (1 - t) ** 3 * np.array(points[0]) +
            3 * (1 - t) ** 2 * t * np.array(points[1]) +
            3 * (1 - t) * t ** 2 * np.array(points[2]) +
            t ** 3 * np.array(points[3])
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verificar si se ha seleccionado un punto de control
            mouse_pos = pygame.mouse.get_pos()
            for i, point in enumerate(self.control_points):
                if pygame.Rect(point[0] - 8, point[1] - 8, 16, 16).collidepoint(mouse_pos):
                    self.selected_point = i
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Soltar el punto de control
            self.selected_point = None

        elif event.type == pygame.MOUSEMOTION and self.selected_point is not None:
            # Mover el punto de control seleccionado
            mouse_pos = pygame.mouse.get_pos()
            self.control_points[self.selected_point] = mouse_pos


# Guardar los puntos de control en un archivo JSON
def save_control_points(curves):
    data = [curve.control_points for curve in curves]
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)


# Cargar los puntos de control desde el archivo JSON si existe
def load_control_points():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    else:
        # Puntos de control iniciales si no hay archivo guardado
        return [
            [(100, 300), (200, 100), (400, 100), (500, 300)],
            [(150, 350), (250, 150), (450, 150), (550, 350)],
            [(200, 400), (300, 200), (500, 200), (600, 400)]
        ]


# Función para dibujar una tabla con coordenadas
def draw_table(curve, curve_index, selected_cell, editing_cell):
    table_x = 50
    table_y = 450 + curve_index * 180
    cell_width = 150
    cell_height = 30

    for i, (x, y) in enumerate(curve.control_points):
        color = curve.color  # Usar el color de la curva para la tabla
        # Dibujar las coordenadas X e Y
        x_text = font.render(f"X: {x}", True, color)
        y_text = font.render(f"Y: {y}", True, color)

        # Dibujar las celdas para X
        cell_rect_x = pygame.Rect(table_x, table_y + i * cell_height, cell_width, cell_height)
        pygame.draw.rect(screen, color, cell_rect_x, 1)
        screen.blit(x_text, (table_x + 5, table_y + i * cell_height + 5))

        # Dibujar las celdas para Y
        cell_rect_y = pygame.Rect(table_x + cell_width, table_y + i * cell_height, cell_width, cell_height)
        pygame.draw.rect(screen, color, cell_rect_y, 1)
        screen.blit(y_text, (table_x + cell_width + 5, table_y + i * cell_height + 5))

        # Resaltar la celda seleccionada
        if selected_cell == (curve_index, i, 'x'):
            pygame.draw.rect(screen, (0, 255, 0), cell_rect_x, 3)
        if selected_cell == (curve_index, i, 'y'):
            pygame.draw.rect(screen, (0, 255, 0), cell_rect_y, 3)

        # Editar la celda seleccionada
        if editing_cell == (curve_index, i, 'x'):
            # Dibujar caja de texto para edición
            pygame.draw.rect(screen, (255, 255, 255), cell_rect_x, 0)
            pygame.draw.rect(screen, (0, 0, 255), cell_rect_x, 2)

        if editing_cell == (curve_index, i, 'y'):
            pygame.draw.rect(screen, (255, 255, 255), cell_rect_y, 0)
            pygame.draw.rect(screen, (0, 0, 255), cell_rect_y, 2)


# Variables para manejar la edición de las tablas
selected_cell = None  # Celda seleccionada para editar
editing_cell = None  # Celda que se está editando
text_input = ''  # Texto ingresado en la celda

# Cargar puntos de control desde el archivo o usar los predeterminados
loaded_control_points = load_control_points()

# Definir las tres curvas Bézier con puntos de control iniciales o cargados
curves = [
    BezierCurve(loaded_control_points[0], RED),
    BezierCurve(loaded_control_points[1], GREEN),
    BezierCurve(loaded_control_points[2], BLUE)
]

# Bucle principal
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill(BLACK)  # Fondo negro

    # Dibujar las curvas
    for curve in curves:
        curve.draw(screen)

    # Dibujar las tablas para cada curva
    for i, curve in enumerate(curves):
        draw_table(curve, i, selected_cell, editing_cell)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Guardar los puntos de control antes de salir
            save_control_points(curves)
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verificar si se ha hecho clic en una celda de la tabla
            mouse_pos = pygame.mouse.get_pos()
            for curve_index, curve in enumerate(curves):
                table_x = 50
                table_y = 450 + curve_index * 180
                cell_width = 150
                cell_height = 30

                for i, (x, y) in enumerate(curve.control_points):
                    # Revisar si se hizo clic en la celda de X
                    if pygame.Rect(table_x, table_y + i * cell_height, cell_width, cell_height).collidepoint(mouse_pos):
                        if selected_cell == (curve_index, i, 'x'):
                            editing_cell = selected_cell  # Comenzar a editar
                            text_input = ''
                        else:
                            selected_cell = (curve_index, i, 'x')

                    # Revisar si se hizo clic en la celda de Y
                    if pygame.Rect(table_x + cell_width, table_y + i * cell_height, cell_width, cell_height).collidepoint(mouse_pos):
                        if selected_cell == (curve_index, i, 'y'):
                            editing_cell = selected_cell  # Comenzar a editar
                            text_input = ''
                        else:
                            selected_cell = (curve_index, i, 'y')

        elif event.type == pygame.KEYDOWN and editing_cell:
            if event.key == pygame.K_BACKSPACE:
                text_input = text_input[:-1]
            elif event.key == pygame.K_RETURN:
                # Guardar el valor ingresado
                curve_index, point_index, coord = editing_cell
                try:
                    new_value = int(text_input)
                    if coord == 'x':
                        curves[curve_index].control_points[point_index] = (new_value, curves[curve_index].control_points[point_index][1])
                    elif coord == 'y':
                        curves[curve_index].control_points[point_index] = (curves[curve_index].control_points[point_index][0], new_value)
                except ValueError:
                    pass  # Si el valor no es válido, ignorar
                editing_cell = None  # Dejar de editar
                selected_cell = None  # Deseleccionar la celda
            else:
                text_input += event.unicode  # Agregar la entrada de texto

        # Pasar el evento de movimiento del ratón a las curvas
        for curve in curves:
            curve.handle_event(event)

    pygame.display.flip()

pygame.quit()
