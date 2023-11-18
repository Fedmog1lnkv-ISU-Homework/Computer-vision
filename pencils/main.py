import os
import re

import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters, measure


def count_pencils_from_image(image_path, show_plot=False):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    binary_image = image < filters.threshold_otsu(image)

    _, label = cv2.connectedComponents(binary_image.astype(np.uint8))

    count_pencils = sum(
        region.perimeter > 2500 and 30 > (region.major_axis_length / region.minor_axis_length) > 15 for region in
        measure.regionprops(label)
    )

    if show_plot:
        draw_pencils_plot(binary_image, label, count_pencils)

    return count_pencils


def draw_pencils_plot(image, label, count_pencils):
    canvas = np.zeros_like(image)

    for region in measure.regionprops(label):
        if region.perimeter > 2500 and 30 > (region.major_axis_length / region.minor_axis_length) > 15:
            coords = region.coords
            canvas[coords[:, 0], coords[:, 1]] = 255

    plt.imshow(image, cmap='gray')
    plt.contour(canvas, colors='red', linewidths=2)
    plt.title(f'{image_path}\nNumber of pencils: {count_pencils}')
    plt.show()


def extract_number_from_filename(filename):
    match = re.search(r'\((\d+)\)', filename)
    return int(match.group(1)) if match else float('inf')


if __name__ == "__main__":
    directory = "files/"
    show_plots = False
    logs = False

    images_paths = sorted([f"{directory}{image_path}" for image_path in os.listdir(directory)],
                          key=lambda x: extract_number_from_filename(x))

    pencils_count = 0

    for image_path in images_paths:
        count_pencils = count_pencils_from_image(image_path, show_plots)
        pencils_count += count_pencils
        if logs:
            print(image_path, count_pencils)

    print("Total pencils:", pencils_count)
