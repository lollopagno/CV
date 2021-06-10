import cv2 as cv
import mediapipe as mp
import time
import numpy as np

cap = cv.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

previous_time = 0

while True:

    success, img = cap.read()

    if success:
        # Frame rete
        current_time = time.time()
        fps = np.divide(1, (current_time - previous_time))
        previous_time = current_time

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        result = pose.process(imgRGB)

        if result.pose_landmarks:
            mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            for _id, lm in enumerate(result.pose_landmarks.landmark):
                r"""
                :param id: id della coordinata
                :param lm: coordinate x,y,z rispetto al piano
                """
                height, width, n_channel = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)

        cv.putText(img, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv.imshow("Image", img)
        cv.waitKey(1)
