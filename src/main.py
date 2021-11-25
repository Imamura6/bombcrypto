from functools import partial
from PIL import ImageGrab
from time import sleep
import signal
import sys
import cv2 as cv

from windowcapture import WindowCapture
from bombcryptobot import BombcryptoBot

def signal_handler(sig, frame):
    wincap.stop()
    bot.stop()
    cv.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    wincap = WindowCapture()
    bot = BombcryptoBot()
    wincap.start()
    bot.start()
    while(True):
        sleep(0.05)
        if wincap.screenshot is not None:
            bot.update_screenshot(wincap.screenshot)
        if cv.waitKey(1) == ord('q'):
            break
    wincap.stop()
    bot.stop()
    cv.destroyAllWindows()
