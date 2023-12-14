import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("/home/srec/Desktop/FaceRPI/visgenex_key.json")
firebase_admin.initialize_app(cred, {"storageBucket": "visgenex.appspot.com"})

def delete_file(file_path):
    try:
        bucket = storage.bucket()
        file_ref = bucket.blob(file_path)
        file_ref.delete()
        print(f"File {file_path} successfully deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
        

def upload_file(local_file_path, destination_file_path):
    try:
        # Get a reference to the storage bucket
        bucket = storage.bucket()

        # Create a blob object with the specified destination file path
        blob = bucket.blob(destination_file_path)

        # Upload the file
        blob.upload_from_filename(local_file_path)

        print("File ",local_file_path," uploaded successfully.")
    except Exception as e:
        print(f"An error occurred during file upload: {e}")
        
Clf_delete = "model/trained_knn_model.clf"
Xsav_delete = "model/X.sav"
Ysav_delete = "model/Y.sav"

file_Clf = "/home/srec/Desktop/FaceRPI/trained_knn_model.clf" 
dest_Clf = "model/trained_knn_model.clf"
file_Ysav = "/home/srec/Desktop/FaceRPI/Y.sav" 
dest_Ysav = "model/Y.sav"
file_Xsav = "/home/srec/Desktop/FaceRPI/X.sav" 
dest_Xsav = "model/X.sav"     


delete_file(Clf_delete)
delete_file(Xsav_delete)
delete_file(Ysav_delete)

upload_file(file_Clf, dest_Clf)
upload_file(file_Xsav, dest_Xsav)
upload_file(file_Ysav, dest_Ysav)


