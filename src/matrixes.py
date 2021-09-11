import numpy as np


# Матрица смещения
from helpers import normalize


def T(v):
    size = v.shape[0]
    shift_mx = np.zeros((size + 1, size + 1))
    np.fill_diagonal(shift_mx, 1)
    shift_mx[:-1, -1] = v

    return shift_mx


# Матрица поворота
# Углы принимаются в радианах
def R(alpha, beta, gamma):
    return Rx(alpha) @ Ry(beta) @ Rz(gamma)


def Rx(a):
    return np.array([[1, 0, 0, 0],
                     [0, np.cos(a), -np.sin(a), 0],
                     [0, np.sin(a), np.cos(a), 0],
                     [0, 0, 0, 1]])


def Ry(a):
    return np.array([[np.cos(a), 0, np.sin(a), 0],
                     [0, 1, 0, 0],
                     [-np.sin(a), 0, np.cos(a), 0],
                     [0, 0, 0, 1]])


def Rz(a):
    return np.array([[np.cos(a), -np.sin(a), 0, 0],
                     [np.sin(a), np.cos(a), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


# Матрица масштабирования
def S(v):
    size = v.shape[0]
    scale_mx = np.zeros((size + 1, size + 1))
    di = np.diag_indices(size + 1)
    scale_mx[di] = np.append(v, [1])

    return scale_mx


# Матрица перехода от локальных координат к мировым
def Mo2w(rot_mx, trans_mx, scale_mx):
    return scale_mx @ rot_mx @ trans_mx


# Матрица поворота для камеры
def Rc(camera, direction_point):
    y = normalize(camera - direction_point)

    b = normalize(np.array([0, 1, 0]) - y[1] * y)
    a = normalize(np.cross(b, y))

    res = np.zeros((4, 4))
    res[:-1, 0] = a
    res[:-1, 1] = b
    res[:-1, 2] = y
    res[3, 3] = 1

    return res


# Матрица перехода от мировых координат к камерным
def Mw2c(camera, direction_point):
    Tc = T(camera * -1)

    return Tc @ Rc(camera, direction_point)


# Матрица перехода к перспективной проекции
# l, r – левая и правая границы области видимости вдоль оси OX;
# b, t – нижняя и верхняя границы области видимости вдоль оси OY;
# n, f – ближняя и дальняя границы области видимости вдоль оси OZ.
def Mproj_perspective(l, r, t, b, n, f):
    return np.array([[(2 * n) / (r - l), 0, (r + l) / (r - l), 0],
                     [0, (2 * n) / (t - b), (t + b) / (t - b), 0],
                     [0, 0, - (f + n) / (f - n), - (2 * f * n) / (f - n)],
                     [0, 0, -1, 0]])


# Матрица перехода к ортогональной проекции
def Mproj_orthographic(l, r, t, b, n, f):
    pass


# Матрица перехода к оконным координатам
def MViewport(width, height):
    v = np.array([width / 2, height / 2])
    Tw = T(v)
    Sw = S(v)

    return Tw @ Sw
    # return np.array([[width / 2, 0, 0, 0],
    #                  [0, -height / 2, 0, 0],
    #                  [0, 0, 1, 0],
    #                  [width / 2, height / 2, 0, 1]])

