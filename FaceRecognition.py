import dlib
import cv2
import sys
import FaceDetection as FD
from deepface import DeepFace


def is_same(img1, img2):
    data = DeepFace.verify(img1, img2, model_name='Facenet', enforce_detection=False)

    return data


if __name__ == "__main__":
    new, img1 = FD.extractface(cv2.imread(r"C:\Users\Gareth\Pictures\Camera Roll\WIN_20240323_13_05_24_Pro.jpg"))
    new, img2 = FD.extractface(cv2.imread(r"C:\Users\Gareth\Pictures\Camera Roll\WIN_20240323_13_05_15_Pro.jpg"))

    print(is_same(img1[0], img2[0]))

    cv2.imshow("face1", img1[0])
    cv2.imshow("face2", img2[0])
    cv2.waitKey(0)
