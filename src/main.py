from PIL import ImageGrab
import cv2 as cv
from time import time
from windowcapture import WindowCapture
from vision import DebugMode, Vision
from bombcryptobot import BombcryptoBot
import os
import pyautogui
from functools import partial
import signal
import sys
from time import sleep, time
import mss

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
