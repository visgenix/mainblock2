import pyrebase

# firebase_config = {
#     "apiKey": "AIzaSyAAnoM81m9-X8IKrpB4w1HxwU9oljjj0Cc",
#     "authDomain": "visgenex.firebaseapp.com",
#     "databaseURL": "https://visgenex-default-rtdb.firebaseio.com/",
#     "storageBucket": "visgenex.appspot.com"
# }
firebase_config = {
  "apiKey": "AIzaSyCXx-CgXZy2ojfwZ2IH0rxIO54au0vT2Ek",
  "authDomain": "visgenex-model.firebaseapp.com",
  "projectId": "visgenex-model",
  "storageBucket": "visgenex-model.appspot.com",
  "databaseURL": "https://visgenex-model-default-rtdb.firebaseio.com/",
  "messagingSenderId": "901577046270",
  "appId": "1:901577046270:web:0710652d0a118b56324daf",
  "measurementId": "G-537DV1ZW9B"
}
firebase = pyrebase.initialize_app(firebase_config)
storage = firebase.storage()
dest_Xsav = "/model/X.sav"     
storage.child(dest_Xsav).download("/home/srec/Desktop/FaceRPI/","X.sav")
dest_Ysav = "/model/Y.sav"     
storage.child(dest_Ysav).download("/home/srec/Desktop/FaceRPI/","Y.sav")
dest_Clf = "/model/trained_knn_model.clf"
storage.child(dest_Clf).download("/home/srec/Desktop/FaceRPI/","trained_knn_model.clf")    
print("File downloaded successfully.")
