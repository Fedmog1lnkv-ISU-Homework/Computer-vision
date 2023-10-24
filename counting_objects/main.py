import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label


def crop_connected_component(img, label_value):
    indices = np.where(img == label_value)
    y_max, y_min = np.max(indices[0]), np.min(indices[0])
    x_max, x_min = np.max(indices[1]), np.min(indices[1])
    return img[y_min:y_max + 1, x_min:x_max + 1] // label_value


def find_unique_components(labeled_img):
    unique_components = []
    component_counts = []

    for label_value in range(1, labels + 1):
        component = crop_connected_component(labeled_img, label_value)
        is_unique = True

        for i, u_component in enumerate(unique_components):
            if u_component.shape == component.shape and np.equal(u_component, component).all():
                component_counts[i] += 1
                is_unique = False
                break

        if is_unique and np.any(component):
            unique_components.append(component)
            component_counts.append(1)

    return unique_components, component_counts


def plot_unique_components(unique_components, component_counts):
    num_unique_components = len(unique_components)
    rows = 2
    cols = num_unique_components // rows + num_unique_components % rows
    fig, axes = plt.subplots(rows, cols, figsize=(12, 8))

    for i, (fig, count) in enumerate(zip(unique_components, component_counts), start=1):
        ax = axes[i // cols, i % cols]
        ax.imshow(fig, cmap='jet', vmin=0, vmax=1)
        ax.set_title(f"Компонента {i}\nКоличество: {count}")
        print(f"Компонента {i}\tКоличество: {count}")
        ax.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    img = np.load("files/ps.npy.txt")
    labeled_img, labels = label(img)
    unique_components, component_counts = find_unique_components(labeled_img)
    plot_unique_components(unique_components, component_counts)
