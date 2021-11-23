from PIL import Image
import cv2 as cv
import numpy as np
from threading import Thread, Lock
from time import sleep
import mss

class WindowCapture:
    stopped = True
    lock = None
    screenshot = None

    def __init__(self):
        self.lock = Lock()

    def get_screenshot(self):
        screen = mss.mss().grab(mss.mss().monitors[0])
        img_pil = Image.frombytes('RGB', screen.size, screen.bgra, 'raw', 'BGRX')
        img_np = np.array(img_pil)
        img = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
        return img

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            sleep(0.05)
            screenshot = self.get_screenshot()
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()
