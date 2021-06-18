import cv2 as cv  # Version 3.4.14.53
import numpy as np
import matplotlib.pyplot as plt


def drawlines(img_1, img_2, lines, pts1, pts2):
    """ img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines """

    r, c = img_1.shape

    img_1 = cv.cvtColor(img_1, cv.COLOR_GRAY2BGR)
    img_2 = cv.cvtColor(img_2, cv.COLOR_GRAY2BGR)

    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())

        x0, y0 = map(int, [0, -r[2] / r[1]])
        x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])

        img_1 = cv.line(img_1, (x0, y0), (x1, y1), color, 1)
        img_1 = cv.circle(img_1, tuple(pt1), 5, color, -1)
        img_2 = cv.circle(img_2, tuple(pt2), 5, color, -1)

    return img_1, img_2


img_1 = cv.imread("img1.jpg", 0)
img_2 = cv.imread("img2.jpg", 0)

# ORB Descriptor
orb = cv.ORB_create()

kp1, des1 = orb.detectAndCompute(img_1, None)
kp2, des2 = orb.detectAndCompute(img_2, None)

# Create dictionary
bf = cv.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

good = []
pts1 = []
pts2 = []

# Get good points
for i, (m, n) in enumerate(matches):
    if m.distance < 0.8 * n.distance:
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)

# Calcola la matrice fondamentale tra i punti corrispondenti in due immagini.
F, mask = cv.findFundamentalMat(pts1, pts2, cv.FM_LMEDS, None, None, None)
pts1 = pts1[mask.ravel() == 1]
pts2 = pts2[mask.ravel() == 1]

# Disegna le linee epipolari per i punti 2
lines1 = cv.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
lines1 = lines1.reshape(-1, 3)
img_5, img_6 = drawlines(img_1, img_2, lines1, pts1, pts2)

# Disegna le linee epipolari per i punti 2
lines2 = cv.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
lines2 = lines2.reshape(-1, 3)
img_3, img_4 = drawlines(img_2, img_1, lines2, pts2, pts1)

plt.subplot(121), plt.imshow(img_5)
plt.subplot(122), plt.imshow(img_3)
plt.show()
