import numpy as np
import zmq
import cv2
from math import pi


def find_contours(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    blured = cv2.medianBlur(b, 17)
    canny = cv2.Canny(blured, 30, 10)
    dilated = cv2.dilate(canny, None, iterations=1)
    contours_frame, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours_frame


def analyze_contours(frame, contours):
    circles = 0
    rects = 0

    for contour in contours:
        if cv2.contourArea(contour) > 50:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)

            (x, y), rad = cv2.minEnclosingCircle(contour)
            center = int(x), int(y)
            rad = int(rad)
            area_rect = cv2.contourArea(box)
            area_circle = pi * rad * rad
            if area_circle < area_rect:
                cv2.circle(frame, center, rad, (0, 0, 255), 2)
                circles += 1
            else:
                rects += 1
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

    return circles, rects


def process_image(frame):
    contours = find_contours(frame)
    circles, rects = analyze_contours(frame, contours)

    cv2.putText(frame, f"Circles: {circles}, Rects: {rects}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Main', frame)

    return circles, rects


def find_objects(addr, is_from_camera=True):
    if not is_from_camera:
        img = cv2.imread(addr)
        count_circles, count_rects = process_image(img)
        cv2.waitKey(0)
        return count_circles, count_rects

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    socket.connect(addr)

    while True:
        buffer = socket.recv()
        arr = np.frombuffer(buffer, np.uint8)
        frame = cv2.imdecode(arr, -1)
        count_circles, count_rects = process_image(frame)
        print(f"Circles: {count_circles}, Rects: {count_rects}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    cv2.namedWindow('Main')

    img_path = "files/img.jpg"
    zmq_addr = "tcp://192.168.0.105:6556"
    from_camera = False

    count_circles, count_rects = find_objects(img_path, from_camera)
    cv2.destroyAllWindows()
    print(f"Circles: {count_circles}, Rects: {count_rects}")
