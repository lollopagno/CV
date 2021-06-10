import cv2 as cv
import numpy as np
import os
from datetime import datetime

PATH_FILE = "info_images.txt"


class Calibration:

    def __init__(self, obj_p, criteria, size_chessboard=(9, 6)):

        self.criteria = criteria
        self.size = size_chessboard

        # Arrays to store object points and image points from all the images.
        self.obj_points = []  # 3d point in real world space. (punti oggetto)
        self.img_points = []  # 2d points in image plane.     (punti immagine)

        self.obj_p = obj_p

        # Create directory
        self.current_date = datetime.now().strftime("%d%m%Y%H%M%S")
        os.mkdir(self.current_date)
        os.mkdir(f"{self.current_date}/View")
        os.mkdir(f"{self.current_date}/Detected")

        # Create file
        open(f"{self.current_date}/{PATH_FILE}", "x")

    def start(self, img_original):
        count = 0
        total_error = 0
        frame_with_chessboard = img_original.copy()
        finish = False

        gray = cv.cvtColor(img_original, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, self.size, None)
        # cv.findCirclesGrid() # per scacchiera con cerchi

        # If found, add object points, image points (after refining them)
        if ret:
            count += 1

            self.obj_points.append(self.obj_p)
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                       self.criteria)  # Aumento la precisione deii corner trovati

            self.img_points.append(corners2)

            # Draw and display the corners
            cv.drawChessboardCorners(frame_with_chessboard, self.size, corners2, ret)  # Disegno il pattern trovato

            # Calibrazione della telecamena
            # Restituisce: la matrice della telecamera, i coeff. di distorsione, i vettori di traslazione e rotazione
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(self.obj_points, self.img_points, gray.shape[::-1], None,
                                                              None)
            # Total error
            mean_error = 0
            for i in range(len(self.obj_points)):
                img_points_2, _ = cv.projectPoints(self.obj_points[i], rvecs[i], tvecs[i], mtx,
                                                   dist)  # Proietta i punti 3D in un immagine planare
                error = cv.norm(self.img_points[i], img_points_2, cv.NORM_L2) / len(img_points_2)
                mean_error += error

            total_error = np.divide(mean_error, len(self.obj_points))
            error_rounded = np.round(total_error, 2)

            if error_rounded <= 0.02:
                print(f"Save file with error: {error_rounded}")
                finish = save_data(count, self.current_date, img_original, frame_with_chessboard, mtx, dist, rvecs,
                                   tvecs)

        return total_error, frame_with_chessboard, finish


def save_data(count, current_date, img_original, img, mtx, dist, rvecs, tvecs):
    r"""
    # TODO documentation
    """
    # Save image

    try:
        cv.imwrite(f"{current_date}/Detected/detected{count}.png", img)
        cv.imwrite(f"{current_date}/View/view{count}.png", img_original)

        info_image = f"{count}- Camera matrix: \n{mtx}\nDist: {dist}\nDist: {dist}\nTvecs: {tvecs}\n"
        pattern_end = "\n\n*************************\n\n"

        file = open(f"{current_date}/{PATH_FILE}", "a")
        file.write(info_image + pattern_end)
        file.close()

        # Save result calibration
        np.savez(f"{current_date}/data", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

    except Exception as e:
        print(e)
        return False

    return True
