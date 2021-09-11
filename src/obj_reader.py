import numpy as np


def parse_obj(file):
    obj_file = open(file, 'r')

    vertices = []
    texture_vertices = []
    faces = []

    for line in obj_file:
        if len(line) == 1:
            continue
        split = line.split()
        if split[0] == "#":
            continue
        elif split[0] == "v":
            vertices.append(list(map(float, split[1:])))
        elif split[0] == "vt":
            texture_vertices.append(list(map(float, split[1:])))
        elif split[0] == "f":
            faces.append([list(map(int, split[1].split("/"))), list(map(int, split[2].split("/"))),
                          list(map(int, split[3].split("/")))])
    obj_file.close()

    return np.array(vertices), np.array(texture_vertices), np.array(faces)
