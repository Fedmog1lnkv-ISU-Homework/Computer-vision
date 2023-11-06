import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops


def count_internal_and_external_regions(image):
    inverted_image = ~image
    labeled_image = label(inverted_image)
    regions = regionprops(labeled_image)

    is_on_boundary = lambda coords, shape: any(y in (0, shape[0] - 1) or x in (0, shape[1] - 1) for y, x in coords)

    count_internal = sum(1 for region in regions if not is_on_boundary(region.coords, image.shape))
    count_external = len(regions) - count_internal

    return count_internal, count_external


def has_vertical_line(region):
    vertical_sum = np.sum(region.image, axis=0)
    return 1 in (vertical_sum // region.image.shape[0])


def recognize_symbol(region):
    if np.all(region.image):
        return "-"

    internals, externals = count_internal_and_external_regions(region.image)

    if internals == 2:
        return "B" if has_vertical_line(region) else "8"

    if internals == 1:
        if externals == 3:
            return "A"
        elif externals == 2:
            center_y, center_x = np.array(region.image.shape) // 2
            return "P" if region.image[center_y, center_x] > 0 else "D"
        else:
            return "0"

    return classify_no_internal_external(region, externals) if internals == 0 else None


def classify_no_internal_external(region, externals):
    if has_vertical_line(region):
        return "1"

    if externals == 2:
        return "/"

    image = region.image[2:-2, 2:-2]
    _, cut_externals = count_internal_and_external_regions(image)

    if cut_externals == 4:
        return "X"

    if cut_externals == 5:
        center_y, center_x = np.array(image.shape) // 2
        return "*" if image[center_y, center_x] > 0 else "W"

    return "*" if externals == 5 else "W"


if __name__ == "__main__":
    image_path = "./files/symbols.png"
    image = plt.imread(image_path)

    binary_image = np.sum(image, axis=2) > 0
    labeled_image = label(binary_image)
    regions = regionprops(labeled_image)

    symbol_counts = {"Not recognized": 0}

    for region in regions:
        symbol = recognize_symbol(region)
        if symbol is not None:
            labeled_image[labeled_image == region.label] = 0

        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1

    total_symbols = sum(symbol_counts.values())
    accuracy = round((1. - symbol_counts["Not recognized"] / total_symbols) * 100, 2)

    print(f"Recognition accuracy: {accuracy}%")
    print(f"Character Statistics: {symbol_counts}")

    plt.imshow(image, cmap="gray")
    plt.show()
