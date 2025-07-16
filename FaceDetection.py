import numpy as np 
import cv2


face_cascade = cv2.CascadeClassifier(r'C:\Users\Gareth\Desktop\NEA\facedetection\haarcascade_frontalface_default.xml')

def extractface(img):
    faces = []
    new = np.copy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cors = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in face_cors:
        if x-5 > 0:
            x = x-5

        if y-5 > 0:
            y = y-5
        
        if x+w+5:
            w = w+5
        
        if y+h+5:
            h = h+5
        cv2.rectangle(new, (x, y), (x + w, y + h), (255, 0, 0), 2)

        faces.append(cv2.resize(img[y:y+h, x:x+w, :], [64, 64]))
    
    return new, faces

if __name__ == "__main__":
    img, faces = extractface(cv2.imread(r"test.jpg"))

    cv2.imshow("img", img)
    i = 0
    for face in faces:
        cv2.imshow("face" + str(i), face)
        i  += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()

