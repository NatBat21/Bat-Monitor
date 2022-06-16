#import libraries
from subprocess import call
from datetime import datetime, timedelta
import logging

# audio settings
# frequency threshold = 10 kHz
# volume threshold = 15 dB
# sample rate = 250,000 Hz
# channel = 1
# length of audio recording = 5 seconds

while (True):
        logging.basicConfig(filename='NatBatAudio.log', format='%(filename)s [%(lineno)d] %(message)s',
                        level=logging.INFO)
        start_now = datetime.now().strftime('%Y%m%d-%H%M%S')
        start_time = datetime.now()
        start = start_time.strftime('%Y-%m-%d %H-%M-%S')
        #name the recording using the date and time
        #output_filename = "/media/usb/" +"Audio-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".wav"
        output_filename = "/home/pi/testing/" +"Audio-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".wav"
        cmd = ['rec', '-c' ,'1', '-r', '250000', output_filename, 'sinc', '10k', 'silence' ,'1', '0.1', '-15d', 'trim', '0', '10']
    
        
        call(cmd)
        
        end_time = start_time + timedelta(seconds=10)
        end = end_time.strftime('%Y-%m-%d %H-%M-%S')
        logging.info("%s ~ %s (%f)" %(start, end,(end_time-start_time).total_seconds()))
        
        print('recording made')