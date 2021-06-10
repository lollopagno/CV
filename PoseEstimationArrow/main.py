import numpy as np
import cv2 as cv

from Calibration import Calibration
from PoseEstimation import PoseEstimation

NAME_WINDOW = "Calibration"


def callback_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Clicked image in position {x, y}")


# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Callback click mouse
cv.namedWindow(NAME_WINDOW)
cv.setMouseCallback(NAME_WINDOW, callback_mouse)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
obj_p = np.zeros((6 * 9, 3), np.float32)
obj_p[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

cap = cv.VideoCapture(0)

# calibration = Calibration(obj_p, criteria=criteria)
pose_estimation = PoseEstimation(obj_p, criteria, 'data.npz')

while True:

    success, frame = cap.read()

    if success:
        cv.imshow(NAME_WINDOW, frame)

        # total_error, img, terminate = calibration.start(frame)
        img = pose_estimation.start(frame)

        cv.imshow(NAME_WINDOW, img)
        cv.waitKey(1)

        # if terminate:
        #    break
