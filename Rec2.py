import cv2
#import os module for reading training data directories and paths
import os
#import numpy to convert python lists to numpy arrays as
#it is needed by OpenCV face recognizers
import numpy as np
import imutils


subjects = ["", "Lina", "Mazhar", "Obama"]
cap = cv2.VideoCapture(0)
frameWidth = 900


def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_alt.xml')

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    if (len(faces) == 0):
        return None, None

    (x, y, w, h) = faces[0]

    return gray[y:y+w, x:x+h], faces[0]

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

#function to draw text on give image starting from
#passed (x, y) coordinates.
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("weight.xml")


#subject
def predict(test_img):
    #make a copy of the image as we don't want to chang original image
    img = test_img.copy()
    #detect face from the image
    face, rect = detect_face(img)

    #predict the image using our face recognizer
    if not face is None:
        label, confidence = face_recognizer.predict(face)

        if (confidence > 75):
            print ("Unkown")
        else:
            label_text = subjects[label]
            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)
            print (label_text)
    else:
        print ("Unkown")

    cv2.imshow('frame',img)
    return img

while(True):

    ret, frame = cap.read()
    frame = imutils.resize(frame, width=frameWidth)
    test_img1 = frame;

    #perform a prediction
    predicted_img1 = predict(test_img1)




cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()





