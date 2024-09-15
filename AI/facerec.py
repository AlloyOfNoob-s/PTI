import face_recognition
import cv2
import datetime
import os
def saveimg():
    cam = cv2.VideoCapture(0)

    if(not cam.isOpened()):
        print("Cannot open camera")
        return
    else:
        print("Camera opened")
        check, frame = cam.read()
        if not check:
            print("Cannot read frame")
            return
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        cv2.imwrite("AI/saved_face/"+timestamp+".jpg",frame)
        return "AI/saved_face/"+timestamp+".jpg"
def preimg():
    cam = cv2.VideoCapture(0)

    if(not cam.isOpened()):
        print("Cannot open camera")
        return
    else:
        print("Camera opened")
        check, frame = cam.read()
        if not check:
            print("Cannot read frame")
            return
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        cv2.imwrite("AI/temp/"+timestamp+".jpg",frame)
        return "AI/temp/"+timestamp+".jpg"
def face_recognize(old,new):
    old_img = face_recognition.load_image_file(old)
    new_img = face_recognition.load_image_file(new)

    old_encode = face_recognition.face_encodings(old_img)[0]
    new_encode = face_recognition.face_encodings(new_img)[0]
    result = face_recognition.compare_faces([old_encode],new_encode)
    return result
def faceid(face):
    face = fr"{face}"
    for data in os.listdir(r"AI\saved_face"):
        data = fr"{data}"
        print(data)
        result = face_recognize(r"AI/saved_face/"+data, face)
        if result is not None and result[0]:
            return True
    return False