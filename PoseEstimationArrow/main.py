import numpy as np
import cv2 as cv
import time
from colorama import Fore
import asyncio

from PoseEstimationArrow import Calibration as cal
from PoseEstimationArrow.PoseEstimation import PoseEstimation
from PoseEstimationArrow import utility

NAME_WINDOW = "Calibration"
clicked_image = 0
minimum_image = 5
errors = np.zeros(minimum_image)

frame = []
calibration = None


def callback_mouse(event, x, y, flag, param):
    global clicked_image, minimum_image, frame, calibration

    if event == cv.EVENT_LBUTTONDOWN:
        print(Fore.GREEN + f"Clicked image in position {x, y}")

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        success, error, img = calibration.start(frame, gray)

        if success:
            errors[clicked_image] = error
            clicked_image += 1
            # img = pose_estimation.start(frame)

        cv.putText(frame, f"{clicked_image}/{minimum_image}", (530, 460), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv.imshow(NAME_WINDOW, img)
        cv.waitKey(1)


async def main():

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    obj_p = np.zeros((6 * 9, 3), np.float32)
    obj_p[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

    # Termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Callback click mouse
    cv.namedWindow(NAME_WINDOW)
    cv.setMouseCallback(NAME_WINDOW, callback_mouse)

    cap = cv.VideoCapture(0)

    calibration = cal.Calibration(obj_p, criteria=criteria)
    # pose_estimation = PoseEstimation(obj_p, criteria, 'data.npz', draw_cube=True)

    previous_time = 0

    mtx_arr = []
    dist_arr = []

    mtx_mean = []
    dist_mean = []

    while True:

        success, frame = cap.read()

        if success:

            await asyncio.create_task(utility.draw_corners_chessboard(frame, criteria, obj_p))

            # Frame rate
            current_time = time.time()
            fps = np.divide(1, (current_time - previous_time))
            previous_time = current_time
            cv.putText(frame, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            if clicked_image < minimum_image:

                cv.putText(frame, f"{clicked_image}/{minimum_image}", (530, 460), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv.imshow(NAME_WINDOW, frame)
                cv.waitKey(1)

            else:

                if len(mtx_arr) == 0:
                    print(Fore.RED + f"Total error: {np.mean(errors)}")
                    mtx_mean, dist_mean = utility.get_matrices(mtx_arr, dist_arr, minimum_image, calibration.current_date)

                # height, width = frame.shape[:2]
                # new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(mtx_mean, dist_mean, (width, height), 1, (width, height))

                # Undistort
                dst = cv.undistort(frame, mtx_mean, dist_mean)  # , None, new_camera_mtx)

                cv.putText(dst, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                cv.imshow('Undistort', dst)
                cv.imshow(NAME_WINDOW, frame)
                cv.waitKey(1)


if __name__ == "__main__":
    asyncio.run(main())
