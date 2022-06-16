#Record video using a circular buffer and a pir sensor

from gpiozero import MotionSensor
import picamera
from datetime import datetime
from time import sleep
import io


#set pin that pir sensor is connected to
pir = MotionSensor(4)

#allow pir to settle
sleep(10)
print('Ready!')

#start recording a circular stream that keeps 20 seconds of video
camera = picamera.PiCamera()
camera.resolution=(1280, 720)
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')

try:
    while True:
        videofilename= "Video-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".h264"
        #videofilename = "Video-{0:%Y}-{0:%m}-{0:%d}-{0:%H}-{0:%M}-{0:%S}.h264".format(datetime.now())
        camera.wait_recording(1)
        pir.wait_for_motion()                       
        print("Motion detected!")
        #Record for another 10 seconds and then save the video
        camera.wait_recording(10)
        stream.copy_to(videofilename, seconds=20) #set number of seconds that need to be copied to video
        print("Recording finished!")
finally:
    camera.stop_recording()