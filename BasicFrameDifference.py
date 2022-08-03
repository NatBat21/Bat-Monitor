#Record a video when motion is detected
#Original motion detection script by brainflakes. Improved by pageauc, peewee2 and Kesthal (www.raspberrypi.org/phpBB3/viewtopic.php?f=43&t=45235)
#Updated to run in python3 by Alexander Baran-Harper (http://thezanshow.com/electronics-tutorials/raspberry-pi/tutorial-17)

#import libraries 
import picamera
from time import sleep
from datetime import datetime
import io
import subprocess
from PIL import Image

#parameters for detecting motion
threshold = 10
sensitivity = 50

#image settings
width = 100
height = 75
Camerasettings = ""

MotionDetected= False
#let camera adjust to brightness
sleep(10)

print("Ready")

videopath= "/home/pi/Videos/"

def captureimage(settings, width, height):
    command = "raspistill %s -w %s -h %s -t 200 -e bmp -n -o -" % (settings, width, height)
    imageData=io.BytesIO()
    imageData.write(subprocess.check_output(command, shell=True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

def motion():
    
    #Capture the first frame
    image1, buffer1 = captureimage(Camerasettings, width, height)
      
    while (True):
      #Capture a second frame
      image2, buffer2 = captureimage(Camerasettings, width, height)
      
      #Calculate the difference in pixels between the two frames
      changedPixels = 0
      for x in range(0, 100):
        for y in range(0, 75):
          #Pick a colour channel to analyse. This is currently set to green (1)
          diff = abs(buffer1[x,y][1] - buffer2[x,y][1])
          if diff > threshold:
            changedPixels += 1
            
      if changedPixels > sensitivity:
        return True #say motion detected if threshold is reached
        
      #Swap the frames
      image1 = image2
      buffer1 = buffer2


def capturevideo(Time, videopath):
    #Use the date and time to name the video
    videoname= "Video-" + Time.strftime("%d.%m.%Y-%H.%M.%S") +".h264"
    with picamera.PiCamera() as camera:
        camera.resolution=(1280, 720)
        camera.start_recording(videopath + videoname)
        camera.wait_recording(10) #record video for 10 seconds
        camera.stop_recording()

def FindTheTime():
    #Get the time so we can name the video
    Time= datetime.now()
    return Time

while True:
    MotionDetected=motion()
    if MotionDetected:
        print("Motion detected. Started recording a video.")
        Time = FindTheTime()
        capturevideo(Time,videopath)
        print("Video recorded.")
