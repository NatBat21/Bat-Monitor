#record an audio file when frequency threshold is reached
#import libraries
from subprocess import call
from datetime import datetime

# frequency threshold = 10 kHz
# volume threshold = 1 %
# channel = 1
# sample rate = 250000 Hz
# length of audio recording = 5 seconds

while (True):
    
        #name file using date and time
        output_filename = "/home/pi/Audio/" +"Audio-" + datetime.now().strftime("%d.%m.%Y-%H.%M.%S") +".wav"
        
        command = ['rec', '-c' ,'1', '-r', '250000', output_filename, 'sinc', '10k', 'silence' ,'1', '0.1', '1%', 'trim', '0', '5']

        call(command)
        
        print('recording made')
