from pyomxplayer import OMXPlayer
from pprint import pprint
import time
omx = OMXPlayer('/home/pi/Videos/at.mp4')
pprint(omx.__dict__)

time.sleep(5)
print('toggling pause')
omx.toggle_pause()

time.sleep(5)
print('toggling pause')
omx.toggle_pause()

time.sleep(5)
print('stopping')
omx.stop()