import cv2 as cv
import pafy
import torch

jackson_hole = "https://youtu.be/1EiC9bvVGnk"  # Jackson Hole (United States)
taipei = "https://youtu.be/XV1q_2Cl6mI"  # Taipei (Taiwan)
okinawa = "https://youtu.be/h0MHEbYz1c8"  # Okinawa (Japan)
busan = "https://youtu.be/pUcWdJoAuyw"  # Busan (Nord Korea)

vPafy = pafy.new(busan)
play = vPafy.getbest(preftype="any")

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # https://github.com/ultralytics/yolov5

h, w = 600, 1000
cap = cv.VideoCapture(play.url)

while True:
    ret, frame = cap.read()

    if ret:
        frame = cv.resize(frame, (w, h))

        results = model(frame)
        cv.imshow('Image', frame)

        if cv.waitKey(20) == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
