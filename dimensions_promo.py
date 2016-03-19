#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     16/03/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import RPi.GPIO as GPIO

# Disabled toypad code because it doesn't work yet
from lego_dimensions_gateway import Gateway
TOYPAD = Gateway()

from pyomxplayer import OMXPlayer
PLAYER = None# Dummy value so we can do 'if player is None:'


# Define GPIO pins the buttons are on
PIN_BUTTON_1 = 5
PIN_BUTTON_2 = 6
PIN_BUTTON_3 = 13
PIN_BUTTON_4 = 19




def flasher(instructions_file_path='led_seq_1.txt'):
    """Send USB commands after specified time periods have passed"""
    # TimeInSeconds:Byte0,Byte1,...Byte31;\r\n
    start_time = time.time()
    with open(instructions_file_path, 'rb') as instructions_file:
        for line in instructions_file:
            line_time_string, byte_array_string = line.split(':')
            line_time = float(line_time_string)
            byte_array_string = byte_array_string.split(';')[0]
            byte_array = []
            for byte_string in byte_array_string.split(','):
                byte_array.append(int(byte_string))

            target_time = start_time + line_time
            while target_time > time.time():
                time.sleep(0.01)
            TOYPAD.dev.write(1, byte_array)
            continue
    return    




def demo_dummy(demo_number):
    # Simulate playing a movie and telling the toypad to do things while the movie plays
    print('Starting demo %s' % (demo_number))
    time.sleep(2)
    print('Finished demo %s' % (demo_number))
    return


def kill_video():
    """Stop any video that is playing."""
    global PLAYER
    print('stopping player')
    TOYPAD.blank_pads()
    if PLAYER is None:
        return
    PLAYER.stop()
    return


def start_video(video_path):
    """Start playing a video, stopping any that is already going"""
    kill_video()
    global PLAYER
    print('starting video: %s' % (video_path))
    PLAYER = OMXPlayer(video_path)
    return


def callback_1(pin):
    start_video(video_path='/home/pi/Desktop/ghostbusters.mp4')
    # TODO blinky toypad LEDs
    TOYPAD.flash_pad(
        pad = 0,
        on_length = 10,
        off_length = 20,
        pulse_count = 100,
        colour = (255,0,0)# RGB
        )
    return


def callback_2(pin):
    start_video(video_path='/home/pi/Desktop/accolades.mp4')
    # TODO blinky toypad LEDs
    print('flasher running')
    flasher(instructions_file_path='led_seq_1.txt')
    return


def callback_3(pin):
    start_video(video_path='/home/pi/Desktop/benny.mp4')
    # TODO blinky toypad LEDs
    return


def callback_4(pin):
    start_video(video_path='/home/pi/Desktop/e3glados.mp4')
    # TODO blinky toypad LEDs
    return


def main():
    try:
        # Setup GPIO pins
        GPIO.setmode(GPIO.BCM)
        # Set pin directions
        GPIO.setup(PIN_BUTTON_1, GPIO.IN)
        GPIO.setup(PIN_BUTTON_2, GPIO.IN)
        GPIO.setup(PIN_BUTTON_3, GPIO.IN)
        GPIO.setup(PIN_BUTTON_4, GPIO.IN)
        # Prepare edge detection for callbacks
        GPIO.add_event_detect(PIN_BUTTON_1, GPIO.RISING)
        GPIO.add_event_detect(PIN_BUTTON_2, GPIO.RISING)
        GPIO.add_event_detect(PIN_BUTTON_3, GPIO.RISING)
        GPIO.add_event_detect(PIN_BUTTON_4, GPIO.RISING)
        # Assign callbacks
        GPIO.add_event_callback(PIN_BUTTON_1, callback_1)
        GPIO.add_event_callback(PIN_BUTTON_2, callback_2)
        GPIO.add_event_callback(PIN_BUTTON_3, callback_3)
        GPIO.add_event_callback(PIN_BUTTON_4, callback_4)

        # Loop to keep the script running
        c = 0
        while c < 1000:
            c += 1
            time.sleep(1)
            continue
    
    except KeyboardInterrupt:
        pass
    print('exiting')
    kill_video()# Make sure no video is left running when we exit
    
    return


if __name__ == '__main__':
    
        main()


