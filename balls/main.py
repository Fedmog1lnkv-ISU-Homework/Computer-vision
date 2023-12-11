from typing import Optional, Any

import cv2
import time
import random

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

bounds = {
    "red": {"lower": (0, 150, 140), "upper": (15, 255, 255)},
    "blue": {"lower": (90, 160, 160), "upper": (110, 255, 255)},
    "green": {"lower": (51, 90, 120), "upper": (70, 255, 255)},
    "yellow": {"lower": (20, 80, 160), "upper": (35, 255, 255)}
}

prev_time = time.time()
curr_time = time.time()
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
radius = 1
d = 5.6 * 10 ** -2


def guess_colors():
    num_balls = random.choice([3, 4])
    colors = ['g', 'y', 'r', 'b']
    random.shuffle(colors)
    chosen_colors = colors[:num_balls]
    return tuple(chosen_colors)


def get_order_ball(green, yellow, red, blue):
    colors = [(green[0][1], 'g') if green else None,
              (yellow[0][1], 'y') if yellow else None,
              (red[0][1], 'r') if red else None,
              (blue[0][1], 'b') if blue else None]

    # Убираем None значения
    colors = [color for color in colors if color is not None]

    colors.sort(key=lambda x: x[0])
    return tuple([color[1] for color in colors])


def ball_detect(bound: str) -> Optional[tuple[tuple[Any, Any], Any]]:
    mask = cv2.inRange(hsv, bounds[bound]['lower'], bounds[bound]['upper'])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            return (curr_x, curr_y), radius

    return None


def check_three_in_row(balls):
    for i in range(len(balls) - 2):
        if balls[i] and balls[i + 1] and balls[i + 2]:
            return True
    return False


def check_four_in_square(balls):
    return all(balls)


guessed_colors = guess_colors()
print(guessed_colors)

while cam.isOpened():
    isVictory = False

    ret, image = cam.read()
    image = cv2.flip(image, 1)
    curr_time = time.time()
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    green_circle, yellow_circle, red_circle, blue_circle = ball_detect('green'), ball_detect('yellow'), ball_detect(
        'red'), ball_detect('blue')

    balls = [green_circle, yellow_circle, red_circle, blue_circle]

    for ball in balls:
        if ball is not None:
            cv2.circle(image, (int(ball[0][0]), int(ball[0][1])), int(ball[1]), (0, 255, 0), 3)
            cv2.circle(image, (int(ball[0][0]), int(ball[0][1])), 3, (255, 255, 255), 3)

    if check_four_in_square([green_circle, yellow_circle, red_circle, blue_circle]):
        ordered_colors = get_order_ball(green_circle, yellow_circle, red_circle, blue_circle)
        if ordered_colors == guessed_colors:
            isVictory = True
    elif check_three_in_row([green_circle, yellow_circle, red_circle, blue_circle]):
        ordered_colors = get_order_ball(green_circle, yellow_circle, red_circle, blue_circle)
        if ordered_colors == guessed_colors:
            isVictory = True

    if isVictory:
        cv2.putText(
            image,
            "Win",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )
    else:
        cv2.putText(
            image,
            "No",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.imshow("Camera", image)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
