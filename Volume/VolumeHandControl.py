import cv2 as cv
import time
import numpy as np
import math
from HandTracking import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

width_cam, height_cam = 640, 360  # 1280, 720

# Camera
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, width_cam)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height_cam)

# Volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Time
previous_time = 0

# Object
detector = htm.HandDetector(detection_confidence=0.7)

while True:

    success, img = cap.read()

    if success:

        # Frame rate
        current_time = time.time()
        fps = np.divide(1, current_time - previous_time)
        previous_time = current_time

        img = detector.find_hands(img)
        lmList = detector.find_position(img, draw=False)  # List with the coordinates of all hand ids
        if len(lmList) != 0:
            # Get specific ids

            x4, y4 = lmList[4][1], lmList[4][2]
            x8, y8 = lmList[8][1], lmList[8][2]

            cx, cy = (x4 + x8) // 2, (y4 + y8) // 2

            cv.circle(img, (x4, y4), 10, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x8, y8), 10, (255, 0, 255), cv.FILLED)

            cv.line(img, (x4, y4), (x8, y8), (255, 0, 255), 3)

            cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

            length = math.hypot(x8 - x4, y8 - y4)  # Multidimensional Euclidean distance

            vol = np.interp(length, [50, 300], [minVol, maxVol])
            print(length, vol)
            volume.SetMasterVolumeLevel(vol, None)

            if length < 50:
                cv.circle(img, (cx, cy), 15, (0, 255, 0), cv.FILLED)

        cv.putText(img, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        cv.imshow("Img", img)
        cv.waitKey(1)
