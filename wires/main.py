import os

import numpy as np
from scipy.ndimage import binary_erosion, label, binary_opening
import matplotlib.pyplot as plt


def analyze_wires(file_path, img_logs=False):
    try:
        data = np.load(file_path)

        # Общее количество проводов - num_features
        labeled_data, num_features = label(data)
        eroded_data = binary_erosion(data, structure=np.ones((3, 1)))

        if img_logs:
            img_show(data, 'The original image')
            img_show(eroded_data, 'Image after erosion')

        wires = {}
        for label_num in range(1, num_features + 1):
            wire_mask = labeled_data == label_num
            print(wire_mask)
            wires[f"Wire {label_num}"] = analyze_individual_wire(wire_mask, img_logs)

        return wires

    except Exception as e:
        print(f"Error: {e}")


def analyze_individual_wire(wire_mask, img_logs=False):
    dilated_wire = binary_opening(wire_mask, structure=np.ones((3, 1)))
    labeled_data, num_features = label(dilated_wire)
    img_show(dilated_wire, "Wire")
    return num_features


def img_show(data, title):
    plt.imshow(data, cmap='gray')
    plt.title(title)
    plt.show()


files_directory = "files"

for file in os.listdir(files_directory):
    if file.endswith(".txt"):
        file_path = os.path.join(files_directory, file)

        print(f"filename: {file}")
        results = analyze_wires(file_path)

        for wire, count in results.items():
            if count == 0:
                print(f"The {wire} is all torn")

            else:
                print(f"{wire}: {count}")
        print()
