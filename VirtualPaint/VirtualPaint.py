import cv2 as cv
import numpy as np
from HandTracking import HandTrackingModule as htm
import time

YELLOW = "Yellow"
YELLOW_COLOR = (0, 255, 255)
RED = "Red"
RED_COLOR = (0, 0, 255)
FUCHSIA = "Fuchsia"
FUCHSIA_COLOR = (255, 0, 255)
DELETE = "Delete"
DELETE_COLOR = (0, 0, 0)

x_previous, y_previous = 0, 0

cap = cv.VideoCapture(0)

detector = htm.HandDetector()

previous_time = 0

mode = YELLOW
draw_color = YELLOW_COLOR

img_canvas = np.zeros(cap.read()[1].shape, np.uint8)

while True:

    success, img = cap.read()

    if success:

        img = cv.flip(img, 1)  # Reverse image

        # Frame rate
        current_time = time.time()
        fps = np.divide(1, current_time - previous_time)
        previous_time = current_time

        # Detect hands
        img = detector.find_hands(img)
        lmList = detector.find_position(img, draw=False)

        if len(lmList) != 0:
            x8, y8 = lmList[8][1], lmList[8][2]
            x12, y12 = lmList[12][1], lmList[12][2]

            fingers_up = detector.fingers_up()

            if fingers_up[1] and fingers_up[2]:
                x_previous, y_previous = 0, 0
                # Selection mode

                # Checking for the click
                if y8 <= 90:
                    if 0 <= x8 <= 140:
                        mode = YELLOW
                        draw_color = YELLOW_COLOR
                    elif 140 < x8 <= 290:
                        mode = RED
                        draw_color = RED_COLOR
                    elif 290 < x8 <= 440:
                        mode = FUCHSIA
                        draw_color = FUCHSIA_COLOR
                    else:
                        draw_color = DELETE_COLOR
                        mode = DELETE

                cv.rectangle(img, (x8, y8 - 25), (x12, y12 + 25), draw_color, cv.FILLED)

            if fingers_up[1] and not fingers_up[2]:
                # Drawing mode
                cv.circle(img, (x8, y8), 15, draw_color, cv.FILLED)

                if x_previous == 0 and y_previous == 0:
                    x_previous, y_previous = x8, y8

                if draw_color == (0, 0, 0):
                    # Delete color
                    cv.line(img, (x_previous, y_previous), (x8, y8), draw_color, 50)
                    cv.line(img_canvas, (x_previous, y_previous), (x8, y8), draw_color, 50)
                else:
                    # Draw color
                    cv.line(img, (x_previous, y_previous), (x8, y8), draw_color, 15)
                    cv.line(img_canvas, (x_previous, y_previous), (x8, y8), draw_color, 15)

                x_previous, y_previous = x8, y8

        img_gray = cv.cvtColor(img_canvas, cv.COLOR_BGR2GRAY)
        _, img_inverse = cv.threshold(img_gray, 50, 255, cv.THRESH_BINARY_INV)
        img_inverse = cv.cvtColor(img_inverse, cv.COLOR_GRAY2BGR)
        img = cv.bitwise_and(img, img_inverse)
        img = cv.bitwise_or(img, img_canvas)

        cv.putText(img, f"FPS: {int(fps)}", (10, 450), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv.circle(img, (65, 45), 30, YELLOW_COLOR, cv.FILLED)
        cv.circle(img, (215, 45), 30, RED_COLOR, cv.FILLED)
        cv.circle(img, (365, 45), 30, FUCHSIA_COLOR, cv.FILLED)
        cv.circle(img, (515, 45), 30, DELETE_COLOR, cv.FILLED)
        #img = cv.addWeighted(img, 0.5, img_canvas, 0.5, 0)
        cv.imshow("Image", img)
        cv.imshow("Canvas", img_canvas)
        cv.waitKey(1)
