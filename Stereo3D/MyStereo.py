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


def create_output(vertices, colors, filename):
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])

    ply_header = '''ply
		format ascii 1.0
		element vertex %(vert_num)d
		property float x
		property float y
		property float z
		property uchar red
		property uchar green
		property uchar blue
		end_header
		'''

    with open(filename, 'w') as f:
        f.write(ply_header % dict(vert_num=len(vertices)))
        np.savetxt(f, vertices, '%f %f %f %d %d %d')


def main():
    mtx, dist = load_data("data/data.npz")

    img_1 = cv.imread("images/img_1.png")
    img_2 = cv.imread("images/img_2.png")

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

    print("\nGenerating the 3D map...")
    # Get new downsampled width and height
    h, w, _ = img_2_down.shape

    # Load focal length.
    focal_length = np.load('data/FocalLength.npy')

    # Perspective transformation matrix
    # This transformation matrix is from the openCV documentation.
    Q = np.float32([[1, 0, 0, -w / 2.0],
                    [0, -1, 0, h / 2.0],
                    [0, 0, 0, -focal_length],
                    [0, 0, 1, 0]])

    # This transformation matrix is derived from Prof. Didier Stricker's power point presentation on computer vision.
    # Link : https://ags.cs.uni-kl.de/fileadmin/inf_ags/3dcv-ws14-15/3DCV_lec01_camera.pdf
    Q2 = np.float32([[1, 0, 0, 0],
                     [0, -1, 0, 0],
                     [0, 0, focal_length * 0.05, 0],  # Focal length multiplication obtained experimentally.
                     [0, 0, 0, 1]])

    # Reproject points into 3D
    points_3D = cv.reprojectImageTo3D(disparity_map, Q2)

    colors = cv.cvtColor(img_1_down, cv.COLOR_BGR2RGB)

    # Get rid of points with value 0 (i.e no depth)
    mask_map = disparity_map > disparity_map.min()

    # Mask colors and points.
    output_points = points_3D[mask_map]
    output_colors = colors[mask_map]

    # Define name for output file
    output_file = 'data/reconstructed.ply'

    # Generate point cloud
    print("\n Creating the output file... \n")
    create_output(output_points, output_colors, output_file)


if __name__ == "__main__":
    main()
