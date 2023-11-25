import numpy as np
import cv2
from skimage.measure import label


def convert_to_gray_and_hsv(image):
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return im_gray, img_hsv


def apply_threshold(im_gray):
    _, im_gray_th_otsu = cv2.threshold(im_gray, 128, 192, cv2.THRESH_OTSU)
    return im_gray_th_otsu


def analyze_segments(labeled, img_hsv):
    results = {}
    rects = 0
    circles = 0

    for segment_index in range(1, np.max(labeled) + 1):
        segment_indices = np.where(labeled == segment_index)

        y_min, x_min = segment_indices[0][0], segment_indices[1][0]
        y_max, x_max = segment_indices[0][-1], segment_indices[1][-1]

        segment_area = (x_max - x_min + 1) * (y_max - y_min + 1)

        figure_type = 'rect' if segment_area == len(segment_indices[0]) else 'circle'
        shade = img_hsv[y_min, x_min, 0]

        results.setdefault(shade, [0, 0])

        figure_index = 0 if figure_type == 'rect' else 1
        results[shade][figure_index] += 1

        if figure_type == 'rect':
            rects += 1
        else:
            circles += 1

    return results, rects, circles



if __name__ == "__main__":
    image_path = "files/balls_and_rects.png"

    image = cv2.imread(image_path)
    im_gray, img_hsv = convert_to_gray_and_hsv(image)
    im_gray_th_otsu = apply_threshold(im_gray)
    labeled = label(im_gray_th_otsu)

    results, rects, circles = analyze_segments(labeled, img_hsv)

    print(f"Total figures: {np.max(labeled)}")
    print(f"Total shades: {len(results)}")
    print(f"Total rectangles: {rects}")
    print(f"Total circles: {circles}")

    print("\nResults by Shade:\n{:<8} {:<12} {:<8}".format("shade", "rectangles", "circles"))
    for hue, counts in results.items():
        print("{:<8} {:<12} {:<8}".format(hue, counts[0], counts[1]))
