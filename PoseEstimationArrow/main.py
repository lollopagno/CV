import numpy as np
import cv2 as cv
import time
from colorama import Fore

from PoseEstimationArrow import Calibration as cal
from PoseEstimationArrow.PoseEstimation import PoseEstimation
from PoseEstimationArrow import utility

NAME_WINDOW = "Calibration"
CALIBRATION = True
clicked_image = 0
minimum_image = 20
errors = np.zeros(minimum_image)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
obj_p = np.zeros((6 * 9, 3), np.float32)
obj_p[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

if CALIBRATION:
    calibration = cal.Calibration(obj_p, criteria=criteria)
else:
    pose_estimation = PoseEstimation(obj_p, criteria, 'data/data.npz', draw_cube=False)

mtx_mean = []
dist_mean = []


def callback_mouse(event, x, y, flag, param):
    global clicked_image, minimum_image, calibration

    if event == cv.EVENT_LBUTTONDOWN:
        frame = calibration.frame
        print(Fore.GREEN + f"Clicked image in position {x, y}")

        success, error, img = calibration.start(frame)

        if success:
            errors[clicked_image] = error
            clicked_image += 1
            # img = pose_estimation.start(frame)

        cv.putText(img, f"{clicked_image}/{minimum_image}", (530, 460), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv.imshow(NAME_WINDOW, img)
        cv.waitKey(1)


def main():
    global clicked_image, minimum_image, calibration, criteria, mtx_mean, dist_mean

    # Callback click mouse
    if CALIBRATION:
        cv.namedWindow(NAME_WINDOW)
        cv.setMouseCallback(NAME_WINDOW, callback_mouse, calibration)

    cap = cv.VideoCapture(0)

    previous_time = 0

    mtx_arr = []
    dist_arr = []

    while True:

        success, frame = cap.read()

        if success:

            # Frame rate
            current_time = time.time()
            fps = np.divide(1, (current_time - previous_time))
            previous_time = current_time
            cv.putText(frame, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            if CALIBRATION:
                # Camera Calibration
                calibration.set_frame(frame.copy())
                utility.draw_corners_chessboard(frame, criteria)

                if clicked_image < minimum_image:

                    cv.putText(frame, f"{clicked_image}/{minimum_image}", (530, 460), cv.FONT_HERSHEY_PLAIN, 2,
                               (0, 255, 0),
                               2)
                    cv.imshow(NAME_WINDOW, frame)
                    cv.waitKey(1)

                else:

                    if len(mtx_arr) == 0:
                        print(Fore.RED + f"Total error: {np.mean(errors)}")
                        mtx_mean, dist_mean = utility.get_mean_matrix_coeff(mtx_arr, dist_arr, minimum_image,
                                                                            calibration.current_date)
                    # Undistort
                    dst = cv.undistort(frame, mtx_mean, dist_mean)

                    cv.putText(dst, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                    cv.imshow('Image', dst)
                    cv.imshow(NAME_WINDOW, frame)
                    cv.waitKey(1)

            else:
                # Pose Estimation
                img = pose_estimation.start(frame)
                cv.imshow("Image", img)
                cv.waitKey(1)


if __name__ == "__main__":
    main()
