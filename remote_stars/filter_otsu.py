import socket
from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
from skimage import filters
from skimage.measure import label, regionprops


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        if packet := sock.recv(n - len(data)):
            data.extend(packet)
        else:
            return None
    return data


def adaptive_threshold_center(image):
    threshold_value = filters.threshold_otsu(image)
    return image > threshold_value


def process_image(host, port, show_plot=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.send(b"get")
        bts = recvall(sock, 40002)

        im1 = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        if show_plot:
            plt.imshow(im1)
            plt.show()

        center_binary = adaptive_threshold_center(im1)

        if show_plot:
            plt.imshow(center_binary)
            plt.show()

        labeled = label(center_binary)
        regs = regionprops(labeled)

        centers = [reg.centroid for reg in regs]
        distance = round(sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2), 1)

        sock.send(f"{distance}".encode())
        print(f"{distance} - {sock.recv(4)}")


if __name__ == "__main__":
    host_address = "84.237.21.36"
    server_port = 5152
    for _ in range(100):
        process_image(host_address, server_port, show_plot=True)
