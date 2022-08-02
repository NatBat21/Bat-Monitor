#import libraries
from subprocess import call
from datetime import datetime

# audio settings
# frequency threshold = 10 kHz
# volume threshold = 50 dB
# sample rate = 250,000 Hz
# channel = 1
# length of audio recording = 5 seconds

while (True):
        #name the recording using the date and time
        #output_filename = "/media/usb/" +"Audio-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".wav"
        output_filename = "/home/pi/testing/" +"Audio-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".wav"
        cmd = ['rec', '-c' ,'1', '-r', '250000', output_filename, 'sinc', '10k', 'silence' ,'1', '0.001', '-50d', 'trim', '0', '10']

        call(cmd)
        
        print('recording made')
