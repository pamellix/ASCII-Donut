import pygame
import math
import colorsys


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
hue = 0

WIDTH = 1920
HEIGHT = 1080

x_start, y_start = 0, 0

x_separator = 10
y_separator = 20

rows = HEIGHT // y_separator
columns = WIDTH // x_separator
screen_size = rows * columns

x_offset = columns / 2
y_offset = rows / 2

A, B = 0, 0  # rotating animation

theta_spacing = 10
phi_spacing = 1 # for faster rotation change to 2, 3 or more, but first change 86, 87 lines as commented

chars = ".,-~:;=!*#$@"  # luminance index

screen = pygame.display.set_mode((WIDTH, HEIGHT))

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
# display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Donut')
font = pygame.font.SysFont('Arial', 18, bold=True)

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def text_display(letter, x_start, y_start):
    text = font.render(str(letter), True, hsv2rgb(hue, 1, 1))
    display_surface.blit(text, (x_start, y_start))

# def text_display(letter, x_start, y_start):
#     text = font.render(str(letter), True, white)
#     display_surface.blit(text, (x_start, y_start))


run = True
while run:

    screen.fill((black))

    z = [0] * screen_size  # Donut. Fills donut space
    b = [' '] * screen_size  # Background. Fills empty space

    # Создаем форму буквы Z
    for j in range(0, 628, theta_spacing):  # from 0 to 2pi
        for i in range(0, 628, phi_spacing):  # from 0 to 2pi
            # Параметрические уравнения для буквы Z
            t = i / 100.0  # параметр от 0 до 2π
            
            # Определяем координаты точек буквы Z
            if t < 1:  # Верхняя горизонтальная линия
                x_z = t * 1.5 - 0.75  # от -0.75 до 0.75 (короче)
                y_z = 1
                z_z = 0
            elif t < 2:  # Диагональная линия
                x_z = 0.75 - (t - 1) * 1.5  # от 0.75 до -0.75
                y_z = 1 - (t - 1) * 2  # от 1 до -1
                z_z = 0
            else:  # Нижняя горизонтальная линия
                x_z = (t - 2) * 1.5 - 0.75  # от -0.75 до 0.75 (такая же длина как верхняя)
                y_z = -1
                z_z = 0
            
            # Добавляем толщину к букве Z
            thickness = 0.3
            offset_x = (j / 100.0 - math.pi) * thickness
            offset_y = math.sin(j) * thickness
            
            # Итоговые координаты с толщиной
            x_final = x_z + offset_x
            y_final = y_z + offset_y
            z_final = z_z
            
            # Применяем вращение
            e = math.sin(A)
            f = math.sin(B)
            g = math.cos(A)
            h = math.cos(B)
            
            # Поворот вокруг осей
            x_rot = x_final * h - y_final * f
            y_rot = x_final * f + y_final * h
            z_rot = z_final * g - y_rot * e
            y_rot = y_rot * g + z_final * e
            
            # Проекция на экран
            D = 1 / (z_rot + 3)  # расстояние до камеры
            x = int(x_offset + 30 * D * x_rot)
            y = int(y_offset + 15 * D * y_rot)
            o = int(x + columns * y)
            
            # Вычисляем освещение
            N = int(8 * (x_rot * 0.5 + y_rot * 0.5 + z_rot * 0.7))
            
            if rows > y and y > 0 and x > 0 and columns > x and D > z[o]:
                z[o] = D
                # Ограничиваем индекс в пределах длины строки символов
                char_index = max(0, min(N, len(chars) - 1))
                b[o] = chars[char_index]

    if y_start == rows * y_separator - y_separator:
        y_start = 0

    for i in range(len(b)):
        A += 0.00002 # замедленное вращение
        B += 0.00001 # замедленное вращение
        if i == 0 or i % columns:
            text_display(b[i], x_start, y_start)
            x_start += x_separator
        else:
            y_start += y_separator
            x_start = 0
            text_display(b[i], x_start, y_start)
            x_start += x_separator


    pygame.display.update()

    hue += 0.005

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False