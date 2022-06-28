#video live stream

from picamera.array import PiRGBArray
import datetime
from picamera import PiCamera
import time
import cv2

#initialise the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

#give the camera time to adjust
time.sleep(0.1)

#capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    #get the NumPy array representing the image and initialise the timestamp
    image = frame.array
    
    #display the frame
    cv2.putText(image, datetime.datetime.now().strftime("%A %d %B %Y %I-%M-%S%p"),
        (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.imshow("Live Camera", image)
    key = cv2.waitKey(1) & 0xFF
    
    #clear the stream for the next frame
    rawCapture.truncate(0)
    
    #if the `q` key is pressed, break
    if key == ord("q"):
        break
        
cv2.destroyAllWindows()
