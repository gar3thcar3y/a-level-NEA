import cv2

rtsp_url = 'http://192.168.1.165:81/stream'

# Capture the video stream
cap = cv2.VideoCapture(rtsp_url)



while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Process the frame with OpenCV here
    cv2.imshow("Face Detection", frame)