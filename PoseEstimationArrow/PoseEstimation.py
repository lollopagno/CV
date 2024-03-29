import numpy as np
import cv2 as cv

axis_arrow = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

axis_cube = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],
                        [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])


def load_data(name_file):
    try:
        with np.load(name_file) as X:
            mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
    except Exception as e:
        with np.load(name_file) as X:
            mtx, dist = [X[i] for i in ('mtx', 'dist')]

    return mtx, dist


def draw_arrow(img, corners, img_pts):
    """
    Draw arrows x, y and z.
    """
    corners = np.int32(corners)
    img_pts = np.int32(img_pts)

    corner = tuple(corners[0].ravel())  # Ravel: 'Fonde' due array monodimensionali.

    img = cv.arrowedLine(img, corner, tuple(img_pts[0].ravel()), (255, 0, 0), 5)
    img = cv.arrowedLine(img, corner, tuple(img_pts[1].ravel()), (0, 255, 0), 5)
    img = cv.arrowedLine(img, corner, tuple(img_pts[2].ravel()), (0, 0, 255), 5)

    return img


def draw_cube(img, img_pts):
    r"""
    Draw cube.
    """
    img_pts = np.int32(img_pts).reshape(-1, 2)

    # Draw ground floor in green
    img = cv.drawContours(img, [img_pts[:4]], -1, (0, 255, 0), -3)

    # Draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv.line(img, tuple(img_pts[i]), tuple(img_pts[j]), 255, 3)

    # Draw top layer in red color
    img = cv.drawContours(img, [img_pts[4:]], -1, (0, 0, 255), 3)
    return img


class PoseEstimation:

    def __init__(self, obj_p, criteria, name_file, size_chessboard=(9, 6), draw_cube=False):
        self.criteria = criteria
        self.mtx, self.dist = load_data(name_file)
        self.size = size_chessboard
        self.obj_p = obj_p
        self.draw_cube = draw_cube

    def start(self, img_original, img_canvas):
        gray = cv.cvtColor(img_original, cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(gray, self.size, None)

        if ret and len(self.mtx) != 0 and len(self.dist) != 0:
            corners_2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)

            # Find the rotation and translation vectors.
            ret, rvecs, tvecs = cv.solvePnP(self.obj_p, corners_2, self.mtx, self.dist)

            if self.draw_cube:
                # Project 3D points to image plane
                img_pts, _ = cv.projectPoints(axis_cube, rvecs, tvecs, self.mtx, self.dist)
                img_original = draw_cube(img_original, img_pts)
                img_canvas = draw_cube(img_canvas, img_pts)
            else:
                # Project 3D points to image plane
                img_pts, _ = cv.projectPoints(axis_arrow, rvecs, tvecs, self.mtx, self.dist)
                img_original = draw_arrow(img_original, corners_2, img_pts)
                img_canvas = draw_arrow(img_canvas, corners_2, img_pts)

        return img_original, img_canvas
