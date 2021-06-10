import cv2 as cv
import time
import numpy as np
from HandTracking import HandTrackingModule as htm
from HandTracking.OpticalFlow import OpticalFlow

cap = cv.VideoCapture(0)

previous_time = 0
detector = htm.HandDetector()

_, first_frame = cap.read()
of = OpticalFlow(first_frame)

while True:
    success, img = cap.read()

    if success:
        # Frame rate
        current_time = time.time()
        fps = np.divide(1, (current_time - previous_time))
        previous_time = current_time

        # Dense optical flow
        img_of = of.start(img)

        # Detector
        detector.find_hands(img, draw=True)
        lm_list = detector.find_position(img, draw=True)

        cv.putText(img, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        cv.imshow("Image", img)
        cv.imshow("Optical Flow", img_of)
        cv.waitKey(1)
