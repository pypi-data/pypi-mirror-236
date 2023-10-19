import cv2
from pyutils.cvfacedetector.facedetector import FaceDetector

face_detector = FaceDetector(confidence=0.5)

img = cv2.imread('pass.png')

faces = face_detector.detectFaces(img)
# foreach face
for face, box, confidence in faces:
    print('face', face.shape)
    print('box', box)
    print('confidence', confidence)
    #draw box on image
    cv2.rectangle(img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0,255,0), 2)
cv2.imshow('face', img)
cv2.waitKey(0)
