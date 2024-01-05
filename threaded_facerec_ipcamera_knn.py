import cv2

import os
import time
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
import numpy as np
from threading import Thread
import pandas as pd
from datetime import datetime
from datetime import date
import pyrebase
from training import training
from git_pull import check_and_pull_repo

# firebaseConfig = { 'apiKey': "AIzaSyDYFlafc3qwcHuq968-sYJKK2zAUv6E6L8",
#   'authDomain': "final-d7d07.firebaseapp.com",
#   'projectId': "final-d7d07",
#   'storageBucket': "final-d7d07.appspot.com",
#   'messagingSenderId': "582443647764",
#   'appId': "1:582443647764:web:8ea0ea34894d1e9971f801",
#   'measurementId': "G-RH6QHL6YBF",
#   'databaseURL':'https://console.firebase.google.com/project/final-d7d07/storage/final-d7d07.appspot.com/files'}

firebaseConfig = {
  'apiKey': "AIzaSyAAnoM81m9-X8IKrpB4w1HxwU9oljjj0Cc",
  'authDomain': "visgenex.firebaseapp.com",
  'databaseURL': "https://visgenex-default-rtdb.firebaseio.com",
  'projectId': "visgenex",
  'storageBucket': "visgenex.appspot.com",
  'messagingSenderId': "87892162499",
  'appId': "1:87892162499:web:288b72916bbe5a13eeaf76"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()




def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time
def get_date():
    today = str(datetime.today().date())
    return today


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG'}
now = datetime.now()
check = now.replace(hour=12, minute=00, second=0, microsecond=0)
Namelst=[]



def predict(X_frame, knn_clf=None, model_path=None, distance_threshold=0.040):

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_frame,num_jitters=2 ,known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings)
    are_matches = [closest_distances[0][i][0]<=distance_threshold  for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else (" ", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def attendance(predictions):
    s_id=predictions[0][0].split("_")[2]
    s_name=predictions[0][0].split("_")[0]
    s_dept=predictions[0][0].split("_")[1]
    #print(s_id,s_name,s_dept)
    header = ['Staff_ID','Staff_Name','Department','Time1','Time2','Time3','Time4','Time5']
    # reading the csv file
    try:
        df = pd.read_csv('/home/srec/Desktop/FaceRPI/data/'+get_date()+".csv")
        #print("read")
    except:
        df = pd.DataFrame(columns=header)
        print("created")
    a=[]
    a=df['Staff_ID'].tolist()
    #print(a)
    if int(s_id) in a:
        n=a.index(int(s_id))
        #updating the column value/data
        if type(df.loc[n, 'Time2'])!=type(datetime.now().strftime("%H:%M")):
            df.loc[n, 'Time2'] = datetime.now().strftime("%H:%M")
        elif type(df.loc[n, 'Time3'])!=type(datetime.now().strftime("%H:%M")):
            df.loc[n, 'Time3'] = datetime.now().strftime("%H:%M")
        elif type(df.loc[n, 'Time4'])!=type(datetime.now().strftime("%H:%M")):
            df.loc[n, 'Time4'] = datetime.now().strftime("%H:%M")
        elif type(df.loc[n, 'Time5'])!=type(datetime.now().strftime("%H:%M")):
            df.loc[n, 'Time5'] = datetime.now().strftime("%H:%M")
        return df
               
    else:
        # add as new row
        df2={'Staff_ID':s_id,'Staff_Name':s_name,'Department':s_dept,'Time1':datetime.now().strftime("%H:%M")}
        df=df.append(df2, ignore_index = True)
        return df
    
def show_prediction_labels_on_image(frame, predictions):

    """
    Shows the face recognition results visually.

    :param frame: frame to show the predictions on
    :param predictions: results of the predict function
    :return opencv suited image to be fitting with cv2.imshow fucntion:
    """
    pil_image = Image.fromarray(frame)

    # Save image in open-cv format to be able to show it.

    time = get_time()
    opencvimage = np.array(pil_image)
    try:
        opencvimage=cv2.putText(opencvimage,predictions[0][0].split("_")[0],(95,115),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
        opencvimage=cv2.putText(opencvimage,predictions[0][0].split("_")[2],(95,155),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
        opencvimage=cv2.putText(opencvimage, time,(95,195),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
        if predictions[0][0]not in Namelst and predictions[0][0] !="unknown":
            df1=attendance(predictions)
            df1.to_csv('/home/srec/Desktop/FaceRPI/data/'+get_date()+".csv",index=False)
            Namelst.append(predictions[0][0])
            print(Namelst)
    except Exception as e:
        print(e)
        Namelst.clear()
    return opencvimage


class WebcamVideoStream:
    def __init__(self, src=0, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE,0)
        self.stream.set(cv2.CAP_PROP_EXPOSURE,0)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    


def Train_Recognize(thresh):
    repo_path = '/home/srec/Desktop/FaceRPI/mb_device2'
    check_and_pull_repo(repo_path)
    repo_path = '/home/srec/Desktop/FaceRPI/model_assets'
    check_and_pull_repo(repo_path)
    #training()
    # process one frame in every 60 frames for speed
    process_this_frame = 59
    print('Setting cameras up...')
    # multiple cameras can be used with the format url = 'http://username:password@camera_ip:port'
    url = 'http://192.168.43.196:8080/video'
    cap = WebcamVideoStream(src=0).start()
    time.sleep(1.0)
    while 1 > 0:
        frame = cap.read()
        #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame, 1)
        img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        #img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        process_this_frame = process_this_frame + 1
        if process_this_frame % 60 == 0:
            predictions1 = predict(img, model_path="/home/srec/Desktop/FaceRPI/model_assets/trained_knn_model.clf", distance_threshold=thresh)
        frame = show_prediction_labels_on_image(frame, predictions1)
        #cv2.resize(frame,(480,320))
        cv2.namedWindow("camera",cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("camera",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        #frame = cv2.rectangle(frame,(90,75),(400,300),(0,255,0),2)        
        # *****
        top_left = (90,45)
        bottom_right = (400,300)
        mask = np.zeros(frame.shape[:2],dtype=np.uint8)
        cv2.rectangle(mask,top_left,bottom_right,255,-1)
        masked_frame = cv2.bitwise_and(frame,frame,mask=mask)
        #frame=cv2.rectangle(frame,(90,75),(400,300),(0,255,0),2)
        cv2.imshow('camera',masked_frame)
        if get_time()=="10:15" or get_time()=="21:30":
            print('time up')
            if get_time()=="10:15":
                break
            elif get_time()=="21:30":
                storage.child("/Attendance/"+get_date()+"_4.csv").put('/home/srec/Desktop/FaceRPI/data/'+get_date()+".csv")
            break
            
        if cv2.waitKey(1)&0xff==27:
            break
    cap.stop()
    cv2.destroyAllWindows()


Train_Recognize(0.037)
os.system("sudo shutdown")
