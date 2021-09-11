import math

import numpy as np


# Умножение матрицы размером 4 на 4 на точку с 3-мя координатами
def apply_mx(mx, p):
    t = np.append(p, [1])
    dp = mx @ t

    return dp[:3]


# Нормализация вектора
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return np.zeros(v.shape)

    return v / norm


# Подсчет координат точки P в барицентрической сисмете координат
# с вершинами треугольника в точках v0, v1, v2
def calc_barycentric_coords(v0, v1, v2, P):
    T = np.array([[v0[0], v1[0], v2[0]],
                  [v0[1], v1[1], v2[1]],
                  [1, 1, 1]])
    X = np.array([P[0], P[1], 1])

    # Если определитель равен 0, то обратной матрицы не существует
    if np.linalg.det(T) == 0:
        return [-1, 1, 1]

    return np.linalg.inv(T) @ X


# Нахождение прямоугольника, ограничиващего треугольник с вершинами v0, v1, v2
def calc_bounding_box(v0, v1, v2):
    xs, ys = [v0[0], v1[0], v2[0]], [v0[1], v1[1], v2[1]]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)

    min_x, max_x = math.floor(min_x), math.ceil(max_x)
    min_y, max_y = math.floor(min_y), math.ceil(max_y)

    return min_x, max_x, min_y, max_y


# face (грань) представлена следующим форматом
# [v_i0, t_i0, vn_i0],
# [v_i1, t_i1, vn_i1],
# [v_i2, t_i2, vn_i3]
# где v_i, t_i, vn_i – индексы (первый элемент - 1)

# Получение вершины грани
def get_face_vertices(face, vertices):
    idxs = face[:, 0] - 1

    return vertices[idxs]


# Получение текстурных вершин грани
def get_texture_vertices(face, texture_vertices):
    idxs = face[:, 1] - 1

    return texture_vertices[idxs]


# Приведение коордиант вершины к типу int
def cast_vertex2int(v):
    return list(map(int, v))
