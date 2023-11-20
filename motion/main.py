import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle as mplCircle
from motion.Circle import Circle


def get_circles_coords(file_path, show_plots=False):
    coords = []

    img = np.load(file_path)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = [contour for contour in contours if
               len(cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)) >= 6]

    if show_plots:
        fig, ax = plt.subplots()
        ax.imshow(img, cmap='gray')
        for circle in circles:
            moments = cv2.moments(circle)
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
            ax.add_patch(mplCircle((center_x, center_y), 10, color='r', fill=False))
        plt.show()

    for circle in circles:
        moments = cv2.moments(circle)
        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])

        coords += [(center_x, center_y)]
    return coords


def process_circle(circle_name, coords, ix_coords, circle, show_logs=False):
    if show_logs:
        print(
            f"{circle_name} last coords: ({circle.last_center_x}, {circle.last_center_y}), coords: {coords[ix_coords]}")
    circle.add_coords(coords[ix_coords])
    coords.pop(ix_coords)


def process_frames(show_plots=False, show_logs=False):
    global circle_1, circle_2, circle_3

    file_paths = [f'files/h_{i}.npy' for i in range(100)]

    circles_coords = get_circles_coords(file_paths[0], show_plots)

    file_paths = file_paths[1:]

    circle_1 = Circle(color=(0, 0, 1), center_x=circles_coords[0][0], center_y=circles_coords[0][1])
    circle_2 = Circle(color=(1, 0, 0), center_x=circles_coords[1][0], center_y=circles_coords[1][1])
    circle_3 = Circle(color=(0, 1, 0), center_x=circles_coords[2][0], center_y=circles_coords[2][1])

    for file_path in file_paths:
        coords = get_circles_coords(file_path, show_plots)
        IX_coords = 0
        threshold = 5
        while len(coords) != 0:
            IX_coords = (IX_coords + 1) % len(coords)
            threshold += 5

            if circle_1.ensure_coords(coords[IX_coords], threshold):
                process_circle("Circle 1", coords, IX_coords, circle_1, show_logs)
            elif circle_2.ensure_coords(coords[IX_coords], threshold):
                process_circle("Circle 2", coords, IX_coords, circle_2, show_logs)
            elif circle_3.ensure_coords(coords[IX_coords], threshold):
                process_circle("Circle 3", coords, IX_coords, circle_3, show_logs)


if __name__ == '__main__':
    circle_1: Circle
    circle_2: Circle
    circle_3: Circle

    process_frames()

    x_coords_1, y_coords_1 = circle_1.get_x_coords(), circle_1.get_y_coords()
    x_coords_2, y_coords_2 = circle_2.get_x_coords(), circle_2.get_y_coords()
    x_coords_3, y_coords_3 = circle_3.get_x_coords(), circle_3.get_y_coords()

    plt.plot(x_coords_1, y_coords_1, label='Circle 1')
    plt.plot(x_coords_2, y_coords_2, label='Circle 2')
    plt.plot(x_coords_3, y_coords_3, label='Circle 3')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Linear graphs of the coordinates of circles')
    plt.legend()

    plt.show()
