
import cv2
import os

from pyutils.cvfacedetector.yunet import YuNet


class FaceDetector:
    def __init__(self, confidence = 0.5):
        base_dirname = os.path.dirname(__file__)
        self.face_detector = YuNet(modelPath=os.path.join(base_dirname, f'face_detection_yunet_2022mar.onnx'), inputSize=[320, 320], confThreshold=confidence, nmsThreshold=0.3, topK=5000, backendId=0, targetId=0)

    # returns a rectangular section of an input image with optional padding
    def get_padded_rect(self, img, roi, padding):
        x, y, w, h = roi
        x1 = x - padding
        y1 = y - padding
        x2 = x + w + padding
        y2 = y + h + padding

        # check for out of bounds coordinates
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 > img.shape[1]:
            x2 = img.shape[1]
        if y2 > img.shape[0]:
            y2 = img.shape[0]


        # if the box is out of bounds, but a square was requested, just take the square of the shorter side
        if (x1 == 0 or x2 == img.shape[1] or y1 == 0 or y2 == img.shape[0]) and w == h:

            if x2 < y2: # width is shorter
                minw = (x2-x1)
                offsetY = int(((y2-y1) - minw) / 2)
                y1 = y1 + offsetY
                y2 = y2 - offsetY

            elif y2 < x2: # height is shorter
                minh = (y2-y1)
                offsetX = int(((x2-x1) - minh) / 2)
                x1 = x1 + offsetX
                x2 = x2 - offsetX              
            
        return img[y1:y2, x1:x2]


    def detectFaces(self, img: cv2.Mat, padding: int = 0):

        results = []
        squareFaceRoi = None

        (origH, origW) = img.shape[: 2]
        
        # convert bgra and bgr to rgb
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        self.face_detector.setInputSize((origW, origH))
        face_list = self.face_detector.infer(img)

        if face_list is not None:
            for face in face_list:
                box = list(map(int, face[:4])) # probably not square
                confidence = face[-1]
                x, y, w, h = box
                
                # get face roi
                # faceRoi = self.get_padded_rect(img, box, padding)

                # create a square box from box
                if w > h:
                    y = y - int((w-h)/2)
                    h = w
                elif h > w:
                    x = x - int((h-w)/2)
                    w = h
                square_box = [x, y, w, h]
                squareFaceRoi = self.get_padded_rect(img, square_box, padding)
                results.append((squareFaceRoi, square_box, confidence))

        return results