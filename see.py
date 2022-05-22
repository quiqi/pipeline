import cv2
url = 'rtsp://admin:123456@192.168.111.2:554/1'
cap = cv2.VideoCapture(url)
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()