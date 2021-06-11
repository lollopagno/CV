import numpy as np
import cv2 as cv
import time

from PoseEstimationArrow import Calibration as cal
from PoseEstimationArrow.PoseEstimation import PoseEstimation

NAME_WINDOW = "Calibration"
clicked_image = 0
minimum_image = 2
errors = np.zeros(minimum_image)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
obj_p = np.zeros((6 * 9, 3), np.float32)
obj_p[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def callback_mouse(event, x, y, flag, param):
    global clicked_image, minimum_image

    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Clicked image in position {x, y}")

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        error, img = calibration.start(frame, gray)
        errors[clicked_image] = error

        # img = pose_estimation.start(frame)

        clicked_image += 1
        cv.putText(frame, f"{clicked_image}/{minimum_image}", (530, 460), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv.imshow(NAME_WINDOW, img)
        cv.waitKey(1)


def draw_corners_chessboard(img, size, ):
    global criteria, obj_p
    obj_points = []
    img_points = []

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, size, None)

    if ret:
        obj_points.append(obj_p)
        corners_2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        img_points.append(corners_2)
        cv.drawChessboardCorners(img, size, corners_2, ret)


# Callback click mouse
cv.namedWindow(NAME_WINDOW)
cv.setMouseCallback(NAME_WINDOW, callback_mouse)
# TODO set callback every frame to draw corners

cap = cv.VideoCapture(0)

calibration = cal.Calibration(obj_p, criteria=criteria)
# pose_estimation = PoseEstimation(obj_p, criteria, 'data.npz', draw_cube=True)

previous_time = 0

while True:

    success, frame = cap.read()

    if success and clicked_image < minimum_image:

        # Frame rate
        current_time = time.time()
        fps = np.divide(1, (current_time - previous_time))
        previous_time = current_time
        cv.putText(frame, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv.putText(frame, f"{clicked_image}/{minimum_image}", (530, 460), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        cv.imshow(NAME_WINDOW, frame)
        cv.waitKey(1)

    else:
        print(errors)
        # TODO check this

        # mtx, dist = cal.load_coefficients(f'{calibration.current_date}/calibration_chessboard.yml')
        # undistort = cv.undistort(img_view, mtx, dist, None, None)
        # cv.imwrite(f'{calibration.current_date}/undist.jpg', undistort)
        # cv.imshow('Undistort', undistort)
        # cv.waitKey(1)
        break
