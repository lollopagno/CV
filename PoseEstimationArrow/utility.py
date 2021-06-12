import numpy as np
import cv2 as cv

async def draw_corners_chessboard(frame, criteria, obj_p, size=(9, 6)):
    obj_points = []
    img_points = []

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, size, None)

    if ret:
        obj_points.append(obj_p)
        corners_2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        img_points.append(corners_2)
        cv.drawChessboardCorners(frame, size, corners_2, ret)


def get_matrices(mtx, dist, min_image, current_date):
    for index in range(0, min_image):
        with np.load(f"{current_date}/Data/data_{index + 1}.npz") as X:
            _mtx, _dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
            mtx.append(_mtx)
            dist.append(_dist)

    mtx_mean = np.zeros((3, 3))
    dist_mean = np.zeros((1, 5))

    counter_mtx = 0
    for element in mtx:
        counter_mtx += 1
        for i in range(_mtx.shape[0]):
            for j in range(_mtx.shape[0]):
                if counter_mtx == len(mtx):
                    try:
                        mtx_mean[i][j] = (element[i][j] + mtx_mean[i][j]) / min_image
                    except:
                        pass
                else:
                    mtx_mean[i][j] = element[i][j] + mtx_mean[i][j]

    counter_dist = 0
    for element in dist:
        counter_dist += 1
        for i in range(_dist.shape[0]):
            for j in range(_dist.shape[1]):
                if counter_dist == len(dist):
                    try:
                        dist_mean[i][j] = (element[i][j] + dist_mean[i][j]) / min_image
                    except:
                        pass
                else:
                    dist_mean[i][j] = element[i][j] + dist_mean[i][j]

    return mtx_mean, dist_mean
