import numpy as np
from matplotlib import pyplot as plt

num_directions_arr = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))


def is_perimeter(y, x):
    directions_counterclockwise = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for dy, dx in directions_counterclockwise:
        neighbor_y, neighbor_x = y + dy, x + dx
        if 0 <= neighbor_x < data.shape[1] and 0 <= neighbor_y < data.shape[0] and data[neighbor_y, neighbor_x] == 0:
            return True
    return False


def neighbors_counterclockwise(y, x, perimeter_points):
    directions_counterclockwise = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    for dy, dx in directions_counterclockwise:
        neighbor_y, neighbor_x = y + dy, x + dx
        if 0 <= neighbor_x < data.shape[1] and 0 <= neighbor_y < data.shape[0] and \
                data[neighbor_y, neighbor_x] == 1 and (neighbor_y, neighbor_x) not in perimeter_points and is_perimeter(
            neighbor_y, neighbor_x):
            num_direction = num_directions_arr.index((dy, dx))
            return neighbor_y, neighbor_x, num_direction

    return None, None, None


def chain(data, show_plot=False):
    start_y, start_x = None, None
    for x in range(data.shape[1]):
        for y in range(data.shape[0]):
            if data[y, x] == 1:
                start_y, start_x = y, x
                break
        if start_y is not None:
            break

    if start_y is None or start_x is None:
        print("There is no starting point.")
        return []

    perimeter_points = set()
    directions = []

    if show_plot:
        plt.ion()
        fig, ax = plt.subplots()

    first_point_added = False

    while True:
        if (y, x) not in perimeter_points:
            if not first_point_added:
                first_point_added = True
            else:
                perimeter_points.add((y, x))

        if show_plot and len(perimeter_points) != 0:
            ax.clear()
            ax.imshow(data, cmap='gray')

            added_points = np.array(list(perimeter_points))
            ax.plot(added_points[:, 1], added_points[:, 0], 'bo', markersize=2)

            plt.pause(0.1)

        y, x, num_direction = neighbors_counterclockwise(y, x, perimeter_points)
        if num_direction is not None:
            directions += [num_direction]

        if y is None or x is None:
            break

        if first_point_added and (y, x) == (start_y, start_x):
            break

    if show_plot:
        plt.ioff()
        plt.show()

    return directions


# data = np.array(
#     [
#         [0, 0, 1, 1, 0, 0, 0],
#         [0, 1, 1, 1, 1, 0, 0],
#         [0, 1, 1, 1, 1, 0, 0],
#         [0, 0, 1, 1, 1, 0, 0],
#         [0, 1, 1, 1, 1, 1, 0],
#         [0, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 0],
#         [0, 1, 1, 1, 1, 0, 0],
#         [0, 0, 1, 1, 0, 0, 0],
#     ]
# )

data = np.zeros((5, 5))
data[1:3, 1:-1] = 1


def curvature(chain):
    result = []
    for i in range(len(chain)):
        if i == len(chain) - 1:
            result.append(chain[i] - chain[0])
        else:
            result.append(chain[i] - chain[i + 1])
    return result


def normalize(chain):
    for i in range(len(chain)):
        chain[i] = chain[i] % 8


chain_n = chain(data, True)
print(chain_n)

chain_n = curvature(chain_n)
print(chain_n)

normalize(chain_n)
print(chain_n)
