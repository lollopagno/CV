import cv2 as cv
from Homography.Edge import Edge

edge_detector = Edge()

path_img = "img2.jpg"

img = cv.imread(f"imgs/{path_img}")
img = cv.resize(img, (500, 500))
img_canny = edge_detector.find_obj(img)
edge_detector.get_obj()

cv.imshow("Image", img)
cv.imshow("Canny", img_canny)
cv.waitKey(0)
