import cv2 as cv
import time
import numpy as np
from PoseEstimation.PoseModule import PoseDetector

cap = cv.VideoCapture(0)
previous_time = 0

detector = PoseDetector()

while True:

    success, img = cap.read()

    if success:
        # Frame rete
        current_time = time.time()
        fps = np.divide(1, (current_time - previous_time))
        previous_time = current_time

        img = detector.find_pose(img, draw=True)
        lm_list = detector.find_position(img, draw=False)

        cv.putText(img, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv.imshow("Image", img)
        cv.waitKey(1)
