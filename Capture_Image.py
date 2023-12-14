import csv

import cv2
import os

import os.path
# counting the numbers


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



# Take image function

def takeImages(Name):




        cam = cv2.VideoCapture(0)
        harcascadePath = "/home/srec/Desktop/FaceRPI/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        os.makedirs("/home/srec/Desktop/FaceRPI/TrainingImage/"+str(Name))

        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                #incrementing sample number
                sampleNum = sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("/home/srec/Desktop/FaceRPI/TrainingImage/"+ str(Name)+"/"+ os.sep +Name + '_' +str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                #display the frame
                cv2.resize(img, (480, 320))
                cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
                cv2.setWindowProperty("camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.imshow('camera', img)
            #wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()



