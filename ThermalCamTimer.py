import cv2
import numpy as np
import time
import datetime

# Read from the thermal camera. The index sometimes changes from 0 to 1 when the pi restarts.
cap = cv2.VideoCapture(0)

# Check if camera has opened successfully
if (cap.isOpened() == False): 
  print("The camera did not open.")

# Set resolutions of frame and convert from float to integer
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#Create VideoWriter object and store the output in a .avi file, named using the date and time
#Set file paths and duration

videopath='/home/pi/testing/'
duration = 20 #in seconds. This is not exact.
end_time= datetime.datetime.now() + datetime.timedelta(seconds=duration)

video_cod = cv2.VideoWriter_fourcc(*'XVID')
video_output= cv2.VideoWriter(videopath + datetime.datetime.now().strftime("%d.%m.%Y-%H.%M.%S") + '.avi',
                      video_cod,
                      20,
                      (frame_width,frame_height))


while datetime.datetime.now() < end_time:
      ret, frame = cap.read()

      if ret == True:
        # Write the frame into the file
        video_output.write(frame)

        # Display the frame 
        cv2.imshow('frame',frame)

        # Press x on keyboard to finish recording
        if cv2.waitKey(1) & 0xFF == ord('x'):
         break
        
     #Break the loop
      else:
        break  

# release video capture and video write objects
cap.release()
video_output.release()
cv2.destroyAllWindows() 

print("Video saved.")
