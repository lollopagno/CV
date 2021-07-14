import pafy
import cv2 as cv

url_taipei = "https://youtu.be/XV1q_2Cl6mI"
url_busan = "https://youtu.be/pUcWdJoAuyw"
url_jackson_hole = "https://youtu.be/1EiC9bvVGnk"

video_pafy = pafy.new(url_jackson_hole)
play = video_pafy.getbest()
cap = cv.VideoCapture(play.url)

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

size_frame = (frame_width, frame_height)

video = cv.VideoWriter('video/jackson_hole.avi', cv.VideoWriter_fourcc(*'MJPG'), 10, size_frame)

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        video.write(frame)
        cv.imshow("OpenCv", frame)
        cv.waitKey(20)

        if 0xFF == ord('q'):
            break

cap.release()
video.release()
cv.destroyAllWindows()
