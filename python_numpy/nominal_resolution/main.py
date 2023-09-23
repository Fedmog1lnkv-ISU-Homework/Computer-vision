import numpy as np
import os
import matplotlib.pyplot as plt


def calculate_nominal_resolution(filename):
    with open(filename, "r") as file:
        max_object_size_mm = float(file.readline())

        image_matrix = []
        for line in file.readlines()[1:]:
            row = [int(value) for value in line.split()]
            image_matrix.append(row)

    image_width_pixels = len(image_matrix[0])

    return max_object_size_mm / image_width_pixels


if __name__ == "__main__":
    files_directory = "files"

    fig, axes = plt.subplots(2, 3, figsize=(8, 6))

    print(f"filename\t\tnominal resolution (mm/pixel)")
    for i, file in enumerate(os.listdir(files_directory)):
        if file.endswith(".txt"):
            file_path = os.path.join(files_directory, file)
            nominal_resolution = calculate_nominal_resolution(file_path)
            print(f"{file}\t\t{nominal_resolution:.2f}")

            row = i // 3
            col = i % 3
            ax = axes[row, col]

            image = np.loadtxt(file_path, skiprows=1)
            ax.imshow(image, cmap='gray')
            ax.set_title(f"{file}\n{nominal_resolution:.2f} mm/pixel", fontsize=10)
            ax.axis("off")

    fig.suptitle("Nominal resolutions", fontsize=14)
    plt.subplots_adjust(top=0.85, hspace=0.3, wspace=0.3)
    plt.show()
