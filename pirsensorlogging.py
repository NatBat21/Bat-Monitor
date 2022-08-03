#pir motion detection record video using circular buffer

from gpiozero import MotionSensor
import picamera
from datetime import datetime, timedelta
import RPi.GPIO as GPIO
from time import sleep
import io
import logging
import gpiozero as gz

#set pin that pir sensor is connected to 
pir = MotionSensor(4)

#allow pir to settle
sleep(5)
print('Ready!')

#set directory for videos
videopath= "/home/pi/testing/"
#videopath="/media/usb/"

#record temperature in log file
temp=gz.CPUTemperature().temperature

#start recording a circular stream that keeps 20 seconds of video
camera = picamera.PiCamera()
camera.resolution=(1280, 720)
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')

try:
    while True:
        logging.basicConfig(filename='NatBatVideo.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)

        #name the video using the date and time
        videofilename = "Video-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".h264"
        camera.wait_recording(1)
        pir.wait_for_no_motion()
        print('No Motion')
        pir.wait_for_motion()                       
        print("Motion detected!")
        #record for 10 seconds after motion is detected
        camera.wait_recording(10)
        stream.copy_to(videopath + videofilename, seconds=20) #set number of seconds that need to be copied to video
        start_time = datetime.now() - timedelta(seconds=20)
        start = start_time.strftime('%Y-%m-%d %H-%M-%S')
        end_time = datetime.now()
        end = end_time.strftime('%Y-%m-%d %H-%M-%S')
        logging.info("%s ~ %s (%f) %s" %(start, end,(end_time-start_time).total_seconds(), temp))
        print("Recording finished!")
        sleep(2)
finally:
    camera.stop_recording()
