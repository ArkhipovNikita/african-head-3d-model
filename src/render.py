from helpers import *


# Алгоритм Брезенхэма для построения проволчной модели
def render_line(pixels, start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Опредляем наклон линнии по горизонтали
    is_steep = abs(dy) > abs(dx)

    # Делаем поворот, если в этом есть необходимость
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # При необходимости меняем начальную и конечную точку местами
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    # Пересчитаем dx, dx, так как возможно произашли изменения
    dx = x2 - x1
    dy = y2 - y1

    # Отслеживая значение ошибки, которое означает — вертикальное расстояние между текущим значением y
    # и точным значением y для текущего x.
    # Всякий раз, когда мы увеличиваем y, мы увеличиваем значение ошибки на величину наклона dx.
    # Если ошибка превысила 1.0, линия стала ближе к следующему y,
    # поэтому мы уменьшаем y на 1.0, одновременно уменьшая значение ошибки на 1.0.
    err = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Ограничивыаем кординату y в рамках квадрата между начальной и конечной точкой
    y = y1
    # Идем вправо по x пока наш пиксель не перестает попадать на линию(проверка по значению ошибки),
    # если значение ощибкти меньше 0Н, то сдвигаем y вниз
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        try:
            pixels[coord[0], coord[1]] = (255, 255, 255)
        except:
            pass
        err -= abs(dy)
        if err < 0:
            y += ystep
            err += dx


def draw_triangle(pixels, vertices, face):
    v0, v1, v2 = get_face_vertices(face, vertices)
    v0, v1, v2 = cast_vertex2int(v0), cast_vertex2int(v1), cast_vertex2int(v2)

    pairs = [(v0, v1), (v0, v2), (v1, v2)]
    for pair in pairs:
        render_line(pixels, pair[0][:2], pair[1][:2])


def render_wire_model(pixels, vertices, faces):
    for i, face in enumerate(faces):
        print(i)
        draw_triangle(pixels, vertices, face)


def render_triangle(pixels, vertices, face, texture_vertices, texture_array, tex_size, z_buffer, camera):
    # Координаты вершин грани
    v0, v1, v2 = get_face_vertices(face, vertices)
    # Координаты вершин текстур грани
    t0, t1, t2 = get_texture_vertices(face, texture_vertices)
    # Координаты ограничивающего прямоугольника
    min_x, max_x, min_y, max_y = calc_bounding_box(v0, v1, v2)

    # Проверка видимости грани с помощью метода back face culling
    # скалярное произведение вектора нормали к грани
    # с вектором направленным от грани к камере должно быть неотриацательным при видимой грани
    normal = np.cross(v1 - v0, v2 - v0)
    normal = normalize(normal)
    # camera_v = normalize(camera - v0)
    camera_v = [0, 0, 1]
    intensity = np.dot(camera_v, normal)

    if intensity < 0:
        return

    # Чем больше значение скалярного произведения, тем меньше угол между векторами или они находятся ближе,
    # поэтому его можно принять за меру освещенности и расчитывать свет по нему
    # intensity принимает значение от 0 до 1
    color = int(intensity * 255)

    # Проходимся по пикселям ограничивающего прямоугольника
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            # Вычисление барецентрические векторы
            barycentric_vec = calc_barycentric_coords(v0, v2, v1, (x, y))

            # Проверка на то, принадлежит ли пиксель треугольнику
            if any(t < 0 for t in barycentric_vec):
                continue

            # Интерполирование вершины в координату текстуры
            # tx = t0[0] + (t2[0] - t0[0]) * barycentric_vec[1] + (t1[0] - t0[0]) * barycentric_vec[2]
            # ty = t0[1] + (t2[1] - t0[1]) * barycentric_vec[1] + (t1[1] - t0[1]) * barycentric_vec[2]

            # Calculate z-buffer depth.
            # Подсчет координаты z пиксели внутри треугольника
            depth = int(v0[2] + (v2[2] - v0[2]) * barycentric_vec[1] + (v1[2] - v0[2]) * barycentric_vec[2])

            try:
                if z_buffer[x, y] < depth:
                    # По координатам t_x, ty берется цвет текстуры и умножается на "мощность" освещения
                    # pixels[x, y] = (
                    #     int(intensity * texture_array[tx, ty][0]), int(intensity * texture_array[tx, ty][1]),
                    #     int(intensity * texture_array[tx, ty][2]))
                    pixels[x, y] = (color, color, color)
                    z_buffer[x, y] = depth
            except:
                pass


def render(pixels, vertices, faces, texture_vertices, texture_array, tex_size, camera, pixels_size):
    z_buffer = np.zeros(pixels_size)
    z_buffer.fill(-1000)
    for i, face in enumerate(faces):
        print(i)
        render_triangle(pixels, vertices, face, texture_vertices, texture_array, tex_size, z_buffer, camera)
