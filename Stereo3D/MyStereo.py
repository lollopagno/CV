import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

r""""
Tutorial : https://becominghuman.ai/stereo-3d-reconstruction-with-opencv-using-an-iphone-camera-part-i-c013907d1ab5
"""


def load_data(name_file):
    with np.load(name_file) as X:
        mtx, dist = [X[i] for i in ('mtx', 'dist')]

    return mtx, dist


def downsample_image(image, reduce_factor):
    for i in range(0, reduce_factor):
        row, col = image.shape[:2]
        image = cv.pyrDown(image, dstsize=(col // 2, row // 2))  # Esegue un blurr e decampiona l'immagine

    return image


def main():
    mtx, dist = load_data("data.npz")

    img_1 = cv.imread("img1.jpg")
    img_2 = cv.imread("img2.jpg")

    height, width, _ = img_1.shape

    new_matrix, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (width, height), 1)

    img_1_undistort = cv.undistort(img_1, mtx, dist, newCameraMatrix=new_matrix)
    img_2_undistort = cv.undistort(img_2, mtx, dist, newCameraMatrix=new_matrix)

    img_1_down = downsample_image(img_1_undistort, 3)
    img_2_down = downsample_image(img_2_undistort, 3)

    win_size = 5  # Finestra da scorrere sull'immagine per normalizzare luminosità e migliorare la trama.
    min_disp = -1  # Minima disparità consentita tra le 2 immagini.
    max_disp = 63  # Massima disparità consentita tra le 2 immagini.
    num_disp = max_disp - min_disp

    stereo = cv.StereoSGBM_create(minDisparity=min_disp,
                                  numDisparities=num_disp,
                                  blockSize=5,
                                  uniquenessRatio=5,
                                  speckleWindowSize=5,
                                  speckleRange=5,
                                  disp12MaxDiff=1,
                                  P1=8 * 3 * win_size ** 2,
                                  P2=32 * 3 * win_size ** 2)

    print("\nComputing the disparity map...")
    disparity_map = stereo.compute(img_1_down, img_2_down)

    plt.imshow(disparity_map, 'gray')
    plt.show()


if __name__ == "__main__":
    main()
