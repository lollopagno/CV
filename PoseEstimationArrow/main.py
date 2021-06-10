import numpy as np
import cv2 as cv
import os
from datetime import datetime

NAME_WINDOW = "Calibration"
PATH_FILE = "info_images.txt"


def callback_mouse(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Clicked image in position {x, y}")


# Size chessboard
sizeChessboard = (9, 6)

# Termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Callback click mouse
cv.namedWindow(NAME_WINDOW)
cv.setMouseCallback(NAME_WINDOW, callback_mouse)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 9, 3), np.float32)
objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space. (punti oggetto)
imgpoints = []  # 2d points in image plane.     (punti immagine)

cap = cv.VideoCapture(0)

# Create directory
curren_date = datetime.now().strftime("%d%m%Y%H%M%S")
os.mkdir(f"{curren_date}")

# Create file
file = open(f"{curren_date}/{PATH_FILE}", "x")

count = 0

while True:

    success, frame = cap.read()

    if success:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow(NAME_WINDOW, frame)


        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, sizeChessboard, None)
        # cv.findCirclesGrid() # per scacchiera con cerchi

        # If found, add object points, image points (after refining them)
        if ret:
            count += 1

            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                       criteria)  # Aumento la precisione deii corner trovati

            imgpoints.append(corners2)

            # Draw and display the corners
            frame_with_chessboard = frame.copy()
            cv.drawChessboardCorners(frame_with_chessboard, sizeChessboard, corners2, ret)  # Disegno il pattern trovato
            cv.imshow(NAME_WINDOW, frame_with_chessboard)

            # Calibrazione della telecamena
            # Restituisce: la matrice della telecamera, i coeff. di distorsione, i vettori di traslazione e rotazione
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

            if ret:
                # Save image
                cv.imwrite(f"{curren_date}/detected{count}.png", frame_with_chessboard)
                cv.imwrite(f"{curren_date}/view{count}.png", frame)

                info_image = f"{count}- Camera matrix: \n{mtx}\nDist: {dist}\nDist: {dist}\nTvecs: {tvecs}\n"
                pattern_end = "\n\n*************************\n\n"

                file = open(f"{curren_date}/{PATH_FILE}", "a")
                file.write(info_image + pattern_end)
                file.close()

        if cv.waitKey(1) & 0xFF == ord('q'):
            break