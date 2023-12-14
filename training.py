import math
import os
from sklearn import neighbors
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder


def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    
    open2= open("/home/srec/Desktop/FaceRPI/model/Y.sav", "rb")
    y = pickle.load(open2)

    open1= open("/home/srec/Desktop/FaceRPI/model/X.sav", "rb")
    X = pickle.load(open1)
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if class_dir not in y:
            if not os.path.isdir(os.path.join(train_dir, class_dir)):
                continue

            # Loop through each training image for the current person
            for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
                image = face_recognition.load_image_file(img_path)
                face_bounding_boxes = face_recognition.face_locations(image)
                print(class_dir)
                if len(face_bounding_boxes) != 1:
                    # If there are no people (or too many people) in a training image, skip the image.
                    if verbose:
                        print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                else:
                    # Add face encoding for current image to the training set
                    X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                    y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    open_file1 = open("/home/srec/Desktop/FaceRPI/model/X.sav", "wb")
    open_file2 = open("/home/srec/Desktop/FaceRPI/model/Y.sav", "wb")
    pickle.dump(X, open_file1)
    pickle.dump(y, open_file2)
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, metric='cosine')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)
    
    #os.chdir('/')
    #s.chdir('/home/srec/Desktop/FaceRPI/')
    #storage.child('trained_knn_model.clf').put('trained_knn_model.clf')
    #storage.child('X.sav').put('X.sav')
    #storage.child('Y.sav').put('Y.sav')
    #os.chdir('/')

    return knn_clf
def training():
    print("Training KNN classifier...")
    classifier = train("/home/srec/FaceRPI/TrainingImage/", model_save_path="trained_knn_model.clf", n_neighbors=2)
    print("Training complete!")
