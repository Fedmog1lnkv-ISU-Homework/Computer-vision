import numpy as np
import os


def read_image_from_file(filename):
    with open(filename, "r") as file:
        lines = file.readlines()[2:]
        image_matrix = [[int(value) for value in line.split()] for line in lines]
        return np.array(image_matrix)


def find_offset(img1, img2):
    corr = np.correlate(img1.ravel(), img2.ravel(), mode='full')

    y, x = divmod(np.argmax(corr), img2.shape[1])
    return y - img1.shape[0] + 1, x - img1.shape[1] + 1


if __name__ == "__main__":
    files_directory = "files"

    img1 = read_image_from_file(f"{files_directory}/img1.txt")
    img2 = read_image_from_file(f"{files_directory}/img2.txt")

    offset = find_offset(img1, img2)
    print(f"The offset is (y, x) = {offset}")
