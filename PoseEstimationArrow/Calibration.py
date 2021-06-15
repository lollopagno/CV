import cv2 as cv
import numpy as np
import os
from datetime import datetime
from colorama import Fore

PATH_FILE = "info.txt"


class Calibration:
    r"""
    Class calibration.
    """

    def __init__(self, obj_p, criteria, size_chessboard=(9, 6)):

        self.frame = []

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
        os.mkdir(f"{self.current_date}/Data")
        os.mkdir(f"{self.current_date}/Yaml")

        self.counter_image = 0

        # Create file
        open(f"{self.current_date}/{PATH_FILE}", "x")

    def start(self):

        error = 0
        frame_with_chessboard = self.frame.copy()

        gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

        # Find the chess board corners
        success, corners = cv.findChessboardCorners(gray, self.size, None)
        # cv.findCirclesGrid() # per scacchiera con cerchi

        # If found, add object points, image points (after refining them)
        if success:
            ret = success
            self.counter_image += 1

            self.obj_points.append(self.obj_p)
            corners_2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1),
                                        self.criteria)  # Aumento la precisione deii corner trovati

            self.img_points.append(corners_2)

            # Draw and display the corners
            cv.drawChessboardCorners(frame_with_chessboard, self.size, corners_2, ret)  # Disegno il pattern trovato

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

            error = np.divide(mean_error, len(self.obj_points))

            print(Fore.WHITE + f"Save file! Error: {error}, Image:{self.counter_image}")
            self.save_data(self.frame, frame_with_chessboard, mtx, dist, rvecs, tvecs)

        return success, error, frame_with_chessboard

    def set_frame(self, frame):
        self.frame = frame

    def save_data(self, img_original, img, mtx, dist, rvecs, tvecs):
        r"""
        Save images, matrixs and coefficients.
        :param img_original: original image.
        :param img: img with chessboard corner.
        :param mtx: matrix
        :param dist: distortion coefficients.
        :param rvecs translation vectors.
        :param tvecs: rotation vectors.
        """

        try:
            cv.imwrite(f"{self.current_date}/Detected/detected{self.counter_image}.png", img)
            cv.imwrite(f"{self.current_date}/View/view{self.counter_image}.png", img_original)

            info_image = f"{self.counter_image}- Camera matrix: \n{mtx}\nDist: {dist}\nDist: {dist}\nTvecs: {tvecs}\n"
            pattern_end = "\n\n*************************\n\n"

            file = open(f"{self.current_date}/{PATH_FILE}", "a")
            file.write(info_image + pattern_end)
            file.close()

            # Save result calibration
            np.savez(f"{self.current_date}/Data/data_{self.counter_image}", mtx=mtx, dist=dist, rvecs=rvecs,
                     tvecs=tvecs)

            save_coefficients(mtx, dist, f"{self.current_date}/Yaml/calibration_{self.counter_image}.yml")

        except Exception as e:
            print(e)


def save_coefficients(mtx, dist, path):
    """Save the camera matrix and the distortion coefficients to given path/file."""

    cv_file = cv.FileStorage(path, cv.FILE_STORAGE_WRITE)
    cv_file.write('Mtx', mtx)
    cv_file.write('Dist', dist)

    cv_file.release()
