import cv2 as cv
import numpy as np
from OpticalFlow.Sparse.optical_flow_sparse import get_cap


def detect_car(img, original):
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(img_gray, 20, 255, cv.THRESH_BINARY)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=4)

    contours, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    for cnt in contours:
        (x, y, w, h) = cv.boundingRect(cnt)
        area = cv.contourArea(cnt)

        if area <= 500:
            continue

        cv.rectangle(original, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv.imshow("Mask motion", opening)


# url_video = "https://thumbs.gfycat.com/LoathsomeFelineAmericanshorthair-mobile.mp4"
# url_video = "https://youtu.be/XV1q_2Cl6mI"  # Taipei
url_video = "https://youtu.be/f1DyY6a44yA"  # Cambridge

show_log = False
height = 512
width = 750

video = get_cap(url_video, height, width)

_, first_frame = video.read()
first_frame = cv.resize(first_frame, (width, height))
prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

# Mask: [HSV Model] hue (direction of car), value (velocity), saturation (unused)
mask_hsv = np.zeros_like(first_frame)  # Each row of mask: (hue  [ANGLE], saturation, value [VELOCITY])
mask_hsv[..., 1] = 255

while video.isOpened():

    ret, frame = video.read()

    if ret:

        frame = cv.bilateralFilter(frame, 9, 75, 75)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.resize(gray, (width, height))
        frame = cv.resize(frame, (width, height))

        # Optical Flow Dense
        flow = cv.calcOpticalFlowFarneback(prev_gray, gray, None, pyr_scale=0.5, levels=5, winsize=11, iterations=5,
                                           poly_n=5, poly_sigma=1.1, flags=0)

        # Magnitude and angle
        magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])

        # Set image hue according to the optical flow direction
        mask_hsv[..., 0] = angle * 180 / np.pi / 2

        # Set image value according to the optical flow magnitude (normalized)
        mask_hsv[..., 2] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)

        if show_log:
            print("Mask")
            print(mask_hsv, end="\n\n\n")
            break

        mask_rgb = cv.cvtColor(mask_hsv, cv.COLOR_HSV2BGR)
        mask = np.zeros_like(frame)
        mask = cv.addWeighted(mask, 1, mask_rgb, 2, 0)

        detect_car(mask, frame)

        dense_flow = cv.addWeighted(frame, 1, mask_rgb, 2, 0)

        # cv.imshow("Dense Optical Flow", dense_flow)
        cv.imshow("Mask", mask)
        cv.imshow("Original", frame)

        # Update frame
        prev_gray = gray

        if cv.waitKey(10) & 0xFF == ord('q'):
            break
