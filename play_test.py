from cv2 import cv2 as cv 
import datetime
import numpy as np
if __name__ == "__main__":
    frameWidth = 640
    frameHight = 480
    faceCascade = cv.CascadeClassifier("Image/haarcascade_frontalface_default.xml")
    cap = cv.VideoCapture("/home/zcy/workloads/video_offloading/testvedio.mp4")
    cap.set(3,frameWidth)
    cap.set(4,frameHight)
    cap.set(10,130)
    time_st = datetime.datetime.now()
    costs = []
    imgs = []
    while True:
        succes , img = cap.read()
        if succes == False:
            break
        
        # img_encode = cv.imencode('.jpg', img)[1].tobytes()
        # data_encode = np.array(img_encode)
        # str_encode = data_encode.tobytes()

        # nparr = np.frombuffer(str_encode, np.uint8)
        # img = cv.imdecode(nparr, cv.IMREAD_COLOR)

        # imgResise = cv.resize(img, (500,400))
        # imgGray = cv.cvtColor(imgResise, cv.COLOR_BGR2GRAY)
        # faces = faceCascade.detectMultiScale(imgResise, 1.1, 4)
        # for (x, y, w, h) in faces:
        #     cv.rectangle(imgResise, (x, y), (x + w, y + h), (255, 0, 0), 1)
        

        # img_encode = cv.imencode('.jpg', imgResise)[1].tobytes()
        # data_encode = np.array(img_encode)
        # str_encode = data_encode.tobytes()

        
        # nparr = np.frombuffer(str_encode, np.uint8)
        # img = cv.imdecode(nparr, cv.IMREAD_COLOR)

        blur = cv.GaussianBlur(img, (3, 3), 0)  
        canny = cv.Canny(blur, 50, 150)  
        # cv2.imshow('1', img)
        # cv2.imshow('canny', canny)
        # cv2.waitKey(0)


        cv.imshow('video', canny)
        if cv.waitKey(1) & 0xFF ==ord('q'):
            break

