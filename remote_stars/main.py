import itertools
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


def find_extrs(img):
    return [
        (i, j)
        for i, j in itertools.product(range(img.shape[0]), range(img.shape[1]))
        if i > 0
           and j > 0
           and i + 1 < img.shape[0]
           and j + 1 < img.shape[1]
           and img[i][j] > img[i - 1][j]
           and img[i][j] > img[i][j - 1]
           and img[i][j] > img[i + 1][j]
           and img[i][j] > img[i][j + 1]
    ]


def process_image(host, port, show_plot=False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.send(b"get")
        bts = recvall(sock, 40002)

        im1 = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        if show_plot:
            plt.imshow(im1)
            plt.show()

        centers = find_extrs(im1)
        distance = round(sqrt((centers[0][0] - centers[1][0]) ** 2 + (centers[0][1] - centers[1][1]) ** 2), 1)

        sock.send(f"{distance}".encode())
        print(f"{distance} - {sock.recv(4)}")


if __name__ == "__main__":
    host_address = "84.237.21.36"
    server_port = 5152
    for _ in range(10):
        process_image(host_address, server_port)
