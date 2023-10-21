import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage


def is_perimeter(y, x):
    directions_clockwise = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dy, dx in directions_clockwise:
        neighbor_y, neighbor_x = y + dy, x + dx
        if neighbor_x >= 0 and neighbor_x < data.shape[1] and neighbor_y >= 0 and neighbor_y < \
                data.shape[0]:
            if data[neighbor_y, neighbor_x] == 0:
                return True
    return False


def neighbors_clockwise(y, x, perimeter_points):
    directions_clockwise = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    # directions_clockwise = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]

    for dy, dx in directions_clockwise:
        neighbor_y, neighbor_x = y + dy, x + dx
        if neighbor_x >= 0 and neighbor_x < data.shape[1] and neighbor_y >= 0 and neighbor_y < \
                data.shape[0]:

            if data[neighbor_y, neighbor_x] == 1 and (
                    neighbor_y, neighbor_x) not in perimeter_points and is_perimeter(neighbor_y, neighbor_x):
                return neighbor_y, neighbor_x

    return None, None


def chain(data):
    for x in range(data.shape[1]):
        for y in range(data.shape[0]):
            if data[y, x] == 1:
                start_y, start_x = y, x
                break
        if start_y is not None:
            break

    perimeter_points = set()

    plt.ion()
    fig, ax = plt.subplots()

    first_point_added = False

    while True:
        if (y, x) not in perimeter_points:
            perimeter_points.add((y, x))
            if not first_point_added:
                first_point_added = True

        print(y, x)

        ax.clear()
        ax.imshow(data, cmap='gray')

        added_points = np.array(list(perimeter_points))
        ax.plot(added_points[:, 1], added_points[:, 0], 'bo', markersize=2)

        plt.pause(0.00000000001)

        y, x = neighbors_clockwise(y, x, perimeter_points)

        if y is None or x is None:
            break

        if first_point_added and (y, x) == (start_y, start_x):
            break

    plt.ioff()
    plt.show()

    return list(perimeter_points)


data = np.array(
    [
        [0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],

    ]
)

print(chain(data))
