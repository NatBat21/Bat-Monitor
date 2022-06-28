#Sunset and sunrise video recordings using triggerable IR lamps and a pir sensor
#Time is checked every 10 minutes

import picamera
from gpiozero import MotionSensor
import datetime
import RPi.GPIO as GPIO
import time
import logging

#set pin that pir sensor is connected to 
pir = MotionSensor(4)

#set pin that IR lamps are connected to  
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

#allow pir sensor to settle
time.sleep(5)
print('Ready!')
time.sleep(5)

#set directory for videos
videopath= "/home/pi/testing/"
#videopath="/media/usb/"

#camera settings
camera = picamera.PiCamera()
camera.resolution=(1280, 720)

#Time to start recording after and stop recording by.
#The format is hour, minute (in 24 hour form).

sunset_start_recording_hour = 21
sunset_start_recording_min = 30
sunset_stop_recording_hour = 23
sunset_stop_recording_min = 00

sunset_start_time=datetime.time((sunset_start_recording_hour),(sunset_start_recording_min))
sunset_end_time=datetime.time((sunset_stop_recording_hour), (sunset_stop_recording_min))

sunrise_start_recording_hour= 4
sunrise_start_recording_min= 30
sunrise_stop_recording_hour= 6
sunrise_stop_recording_min= 00

sunrise_start_time=datetime.time((sunrise_start_recording_hour), (sunrise_start_recording_min))
sunrise_end_time=datetime.time((sunrise_stop_recording_hour),(sunrise_stop_recording_min))


def check_time(sunrise_start_time, sunrise_end_time, sunset_start_time, sunset_end_time):
    check_time = datetime.datetime.now().time()
    if ((sunrise_start_time <= check_time and check_time <= sunrise_end_time) or 
        (sunset_start_time <= check_time and check_time <= sunset_end_time)):
        return True
    else:
        return False

while True:
   #Check the time falls between set hours
   print("Checking the time...")
   result = check_time(sunrise_start_time, sunrise_end_time, sunset_start_time, sunset_end_time)

   if result:
        logging.basicConfig(filename='NatBatFlashVideo.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)

        #name the video using the date and time
        videofilename = "Video-" + datetime.datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".h264"
        pir.wait_for_no_motion()
        print('No Motion')
        pir.wait_for_motion()
        print("Motion detected!")
        
        #record for 10 seconds after motion is detected and keep IR lights on
        GPIO.output(27, GPIO.HIGH)
        camera.start_recording(videopath + videofilename)
        time.sleep(10)
        camera.stop_recording()
        GPIO.output(27, GPIO.LOW)
        
        #logging parameters
        start_time = datetime.datetime.now() - datetime.timedelta(seconds=10)
        start = start_time.strftime('%Y-%m-%d %H-%M-%S')
        end_time = datetime.datetime.now()
        end = end_time.strftime('%Y-%m-%d %H-%M-%S')
        logging.info("%s ~ %s (%f)" %(start, end,(end_time-start_time).total_seconds()))
        print("Recording finished!")
        time.sleep(2)
   else:
        time.sleep(600)
        
        
