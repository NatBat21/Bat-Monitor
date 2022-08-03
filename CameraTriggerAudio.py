#Record a video and audio file when motion is detected
#Original motion detection script by brainflakes. Improved by pageauc, peewee2 and Kesthal (www.raspberrypi.org/phpBB3/viewtopic.php?f=43&t=45235)
#Updated to run in python3 by Alexander Baran-Harper (http://thezanshow.com/electronics-tutorials/raspberry-pi/tutorial-17)

#import libraries
import picamera
from time import sleep
from datetime import datetime
import io
import subprocess
from PIL import Image
from subprocess import call
from multiprocessing import Process
import sounddevice as sd
import soundfile as sf

#parameters for detecting motion
threshold = 10
sensitivity = 50

#parameters for audio recording
samplerate = 250000 #in Hz
duration = 10 #in seconds


#image settings
width = 100
height = 75
Camerasettings = ""

MotionDetected= False
#let camera adjust to brightness
sleep(2)

print("Ready")

videopath= "/home/pi/Videos/"
audiopath= "/home/pi/Audio/"

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


def capturevideo():
    #Use the date and time to name the video
    videoname= "Video-" + Time.strftime("%d.%m.%Y-%H.%M.%S") +".h264"
    with picamera.PiCamera() as camera:
        camera.resolution=(1280, 720)
        camera.start_recording(videopath + videoname)
        camera.wait_recording(10) #record video for 10 seconds
        camera.stop_recording()
        
def captureaudio():
    #Use the date and time to name the audio file
    audioname = audiopath +"Audio-" + Time.strftime("%d.%m.%Y-%H.%M.%S") +".wav"
    #record a 10 second audio file
    soundcommand= ['rec', '-c' ,'1', '-r', '250000', audioname, 'trim', '0', '10']
    call(soundcommand)

#def captureaudio():
    #audioname = audiopath +"Audio-" + Time.strftime("%d.%m.%Y-%H.%M.%S") +".wav"
    #soundrecording= sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, blocking=True) 
    #sf.write(audioname, soundrecording, samplerate)
    
def FindTheTime():
    #Get the time so we can name the video
    Time= datetime.now()
    return Time

while True:
    MotionDetected=motion()
    if MotionDetected:
        print("Motion detected. Started recording a video.")
        Time = FindTheTime()
        Process(target= capturevideo).start()
        Process(target= captureaudio).start() 
        sleep(11)
        print("Video recorded.")
        print("Audio recorded.")




