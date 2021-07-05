import cv2 as cv


def set_text(img, text, pos, font=cv.FONT_HERSHEY_PLAIN, dim=2, color=(255, 0, 255), thickness=2):
    cv.putText(img, text, pos, font, dim, color, thickness)
