import cv2

import numpy as np

# Load the cascade
face_cascade = cv2.CascadeClassifier(r'C:\Users\Gareth\Desktop\NEA\face_detection\haarcascade_frontalface_default.xml')

# Read the input image
img = cv2.imread(r'C:/Users/Gareth/Desktop/NEA/face_detection/shutterstock_236097745.jpg')

faces = []


if img is None:
    print("Error: Could not open or read the image.")
else:
    cv2.imshow('Original', img)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_cors = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces
    for (x, y, w, h) in face_cors:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        faces.append(img[y:y+h, x:x+w, :])

    # Display the output
    i = 0
    for face in faces:
        print(face)
        try:
            cv2.imshow(str(i), face)
        except:
            pass
        i += 1

    cv2.imshow('img', img)
    cv2.waitKey(0)



# Close all OpenCV windows
cv2.destroyAllWindows()