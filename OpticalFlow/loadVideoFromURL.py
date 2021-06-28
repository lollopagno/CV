import cv2 as cv
import numpy as np
import pafy
import time
from OpticalFlow.Video import Video
from OpticalFlow.Yolo import Yolo

# from OpticalFlow.darkflow.darkflow.net.build import TFNet

h, w = 600, 1000


def frame_rate(previous_time):
    current_time = time.time()
    fps = np.divide(1, (current_time - previous_time))

    return fps, current_time


def openCvProcessing(saved_video_file="yolo/temp.ts", run_yolo=True):
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # https://github.com/ultralytics/yolov5

    # YOLO Model
    # options = {
    #     'model': "darkflow/cfg/yolo.cfg",
    #     'load': "yolo/yolov2.weights",
    #     'threshold': 0.3
    # }

    # tfnet = TFNet(options)  # https://github.com/thtrieu/darkflow

    # colors = [tuple(255 * np.random.rand(3)) for i in range(5)]

    yolo = Yolo()
    yolo.load_yolo()

    cap = cv.VideoCapture(saved_video_file)
    previous_time = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:

            # Frame rate
            fps, previous_time = frame_rate(previous_time)

            if run_yolo:
                yolo.load_image(frame)
                yolo.detect_objects()
                yolo.get_box_dimensions()
                yolo.draw_labels()

            # results = tfnet.return_predict(frame)
            #
            # for color, result in zip(colors, results):
            #     tl = (result['topleft']['x'], result['topleft']['y'])
            #     br = (result['bottomright']['x'], result['bottomright']['y'])
            #
            #     label = result['label']
            #
            #     frame = cv.cv2.rectangle(frame, tl, br, color, 7)
            #     frame = cv.cv2.putText(frame, label, tl, cv.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)

            # cv.cv2.imshow('Image', frame)

            img = frame.copy()
            img = cv.resize(img, (w, h))
            cv.putText(img, f"FPS: {int(fps)}", (10, 35), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

            cv.imshow("Image", img)

            if cv.waitKey(20) == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    jackson_hole = "https://youtu.be/1EiC9bvVGnk"  # Jackson Hole (United States)
    taipei = "https://youtu.be/XV1q_2Cl6mI"  # Taipei (Taiwan)
    okinawa = "https://youtu.be/h0MHEbYz1c8"  # Okinawa (Japan)
    busan = "https://youtu.be/pUcWdJoAuyw"  # Busan (Nord Korea)

    video = Video(url=taipei)

    # video = pafy.new(taipei)
    # play = video.getbest()
    # input: play.url (to openCvProcessing function)

    #video.dl_stream(3)
    openCvProcessing(saved_video_file=0)

# Classes : car, bus, truck
