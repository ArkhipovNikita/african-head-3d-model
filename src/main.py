from math import radians

import numpy as np
from PIL import Image

from helpers import apply_mx
from matrixes import MViewport, Mw2c, Mproj_perspective, S, T, R, Mo2w
from obj_reader import parse_obj
from render import render, render_wire_model

# КОНСТАНТЫ

# Ширина и высота экрана
width, height = 600, 600

# Камера и точка, куда она направлена
camera = np.array([2, 2, 2])
camera_direction = np.array([-2, -2, 0])

# Параметры для перехода в мировые координаты
transition_vec = np.array([-1, 0, 2])
rot_angles = np.array([radians(5), radians(10), radians(15)])
scale_params = np.array([0.8, 0.8, 0.8])

# Пути к файлам модели и текстуры
obj_file_path = '../obj/african_head/african_head.obj'
texture_file_path = '../obj/african_head/african_head_diffuse.tga'

# Выходное изображание
img = Image.new('RGB', (width, height), 'black')
pixels = img.load()


# ЧТЕНИЕ

# Чтение файла модели
vertices, texture_vertices, faces = parse_obj('../obj/african_head/african_head.obj')

# Чтение файла текстуры
texture = Image.open('../obj/african_head/african_head_diffuse.tga')
texture = texture.rotate(180)
tex_size = texture.size
texture_array = texture.load()


# ПРЕОБРАЗОВАНИЕ ВЕРШИН

# Масштабирование координат текстурных вешин до размера текстуры,
# так как изначально вершины представлены в диапозоне от -1 до 1
s = S(np.array([tex_size[0]] * 3))
for t_v in texture_vertices:
    t = np.append(t_v, [1])
    t = s @ t
    t_v[:3] = t[:3]


# Преобразования вершин модели
trans_mx = T(transition_vec)
scale_mx = S(scale_params)
rot_mx = R(*rot_angles)

l2w_mx = Mo2w(trans_mx, scale_mx, rot_mx)
w2c_mx = Mw2c(camera, camera_direction)
proj_mx = Mproj_perspective(-500, 500, -500, 500, 300, -300)
viewport_mx = MViewport(width, height)

for v in vertices:
    # v[:3] = apply_mx(l2w_mx, v)
    # v[:3] = apply_mx(w2c_mx, v)
    # v[:3] = apply_mx(proj_mx, v)

    v[:2] = apply_mx(viewport_mx, v[:2])[:2]
    # масшатбирование z координаты
    v[2] = (v[2] + 1) * (width / 2)

# РЕНДЕРИНГ
render(pixels, vertices, faces, texture_vertices, texture_array, tex_size, camera, (width, height))
# render_wire_model(pixels, vertices, faces)


# СОХРАНЕНИЕ КАРТИНКИ
img = img.rotate(180)
img.save('result/test/1.bmp')


# Для получения "белой" картинки из папки base необходимо закомментировать:
# 1. 3 матричных преобразования с 68 по 70 строки
# 2. убедиться, что 82 и 77 строка раскомментрована
# 3. в функции render_triangle camera_v сделать равным [0, 0, 1]
# 4. в функции render_triangle закомметировать строки, касающиеся окраски в текстуру
