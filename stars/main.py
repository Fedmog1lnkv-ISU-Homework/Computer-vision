import numpy as np
from skimage.measure import label
from skimage.morphology import binary_erosion


def count_objects_by_mask(image, mask):
    labelled_data = label(image)

    result = label(binary_erosion(labelled_data, mask))
    return len(np.unique(result)) - 1


plus_mask = np.array([[0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0],
                      [1, 1, 1, 1, 1],
                      [0, 0, 1, 0, 0],
                      [0, 0, 1, 0, 0]])

cross_mask = np.array([[1, 0, 0, 0, 1],
                       [0, 1, 0, 1, 0],
                       [0, 0, 1, 0, 0],
                       [0, 1, 0, 1, 0],
                       [1, 0, 0, 0, 1]])

data = np.load("files/stars.npy")

print(f"Number of stars: {count_objects_by_mask(data, plus_mask) + count_objects_by_mask(data, cross_mask)}")
