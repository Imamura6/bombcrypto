import logging
import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from vision import DebugMode, Vision

class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    REFRESH_HEROES = 2
    ERROR = 3
    CONNECT_WALLET = 4
    SELECT_WALLET = 5
    SIGN_IN = 6
    TREASURE_HUNT = 7
    NEXT_MAP = 8

class BombcryptoBot:
    REFRESH_HEROES_TIMEOUT_SEC = 900
    LOADING_SCREEN_TIMEOUT_SEC = 300
    lock = None
    state = None
    screenshot = None
    refresh_time = 0
    loading_time = 0

    def __init__(self):
        self.lock = Lock()
        logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)

        self.state = BotState.INITIALIZING
        self.loading_vision = Vision('img/loading_page.PNG')

        self.error_vision = Vision('img/error.PNG')
        self.ok_error_vision = Vision('img/ok_error.PNG')

        self.connect_wallet_vision = Vision('img/connect_wallet.PNG')
        # self.select_wallet_vision = Vision('img/select_wallet.PNG')
        self.sign_in_vision = Vision('img/sign_in.PNG')
        self.treasure_hunt_vision = Vision('img/treasure_hunt.PNG')

        self.sleep_vision = Vision('img/sleep.PNG')
        self.back_vision = Vision('img/back.PNG')
        self.heroes_vision = Vision('img/heroes.PNG')
        self.work_vision = Vision('img/work.PNG')
        self.exit_vision = Vision('img/exit.PNG')
        self.next_map_vision = Vision('img/new_map.PNG')

    def change_state(self, state):
        self.lock.acquire()
        self.state = state
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def move_and_click(self, position):
        while pyautogui.position() != position:
            pyautogui.moveTo(position)
            if pyautogui.position() == position:
                pyautogui.click()
                return

    def check_error(self):
        if self.error_vision.find(self.screenshot, 0.9):
            logging.debug("Error found")
            self.change_state(BotState.ERROR)
            sleep(2)
        elif self.state == BotState.ERROR:
            self.change_state(BotState.SEARCHING)

    def check_loading_page(self):
        if self.loading_vision.find(self.screenshot, 0.9):
            if self.loading_time != 0:
                if time() - self.loading_time > self.LOADING_SCREEN_TIMEOUT_SEC:
                    logging.debug("Refreshing loading screen")
                    points = self.loading_vision.find(self.screenshot, 0.9)
                    self.move_and_click(points[0])
                    sleep(0.2)
                    pyautogui.hotkey('f5')
                    pyautogui.hotkey('f5')
                    sleep(1)
                    self.loading_time = 0
                    self.change_state(BotState.SEARCHING)
            else:
                logging.debug("Start loading screen timer")
                self.loading_time = time()
        elif self.loading_time != 0:
            self.loading_time = 0
            self.change_state(BotState.SEARCHING)

    def search(self):
        if self.connect_wallet_vision.find(self.screenshot, 0.9):
            self.change_state(BotState.CONNECT_WALLET)
        if self.next_map_vision.find(self.screenshot, 0.9):
            self.change_state(BotState.NEXT_MAP)
        if self.sleep_vision.find(self.screenshot, 0.85) and time() - self.refresh_time > self.REFRESH_HEROES_TIMEOUT_SEC:
            self.change_state(BotState.REFRESH_HEROES)

    def wait_for_vision_find(self, vision_object):
        while not vision_object.find(self.screenshot, 0.85):
            if self.state == BotState.ERROR:
                return False
            sleep(0.05)
        return True

    def error(self):
        if self.ok_error_vision.find(self.screenshot, 0.9):
            points = self.ok_error_vision.find(self.screenshot, 0.9)
            self.move_and_click(points[0])
            logging.debug("Ok error {}".format(points[0]))
        elif self.exit_vision.find(self.screenshot, 0.9):
            points = self.exit_vision.find(self.screenshot, 0.9)
            self.move_and_click(points[0])
            sleep(0.2)
            pyautogui.hotkey('f5')
            pyautogui.hotkey('f5')
            logging.debug("Exit error{}".format(points[0]))
        sleep(2)

    def connect_wallet(self):
        points = self.connect_wallet_vision.find(self.screenshot, 0.9)
        self.move_and_click(points[0])
        logging.debug("Connected {}".format(points[0]))

    # def select_wallet(self):
    #     if self.wait_for_vision_find(self.select_wallet_vision):
    #         points = self.select_wallet_vision.find(self.screenshot, 0.9)
    #         self.move_and_click(points[0])
    #         logging.debug("Wallet Selected {}".format(points[0]))

    def sign_in(self):
        if self.wait_for_vision_find(self.sign_in_vision):
            points = self.sign_in_vision.find(self.screenshot, 0.9)
            self.move_and_click(points[0])
            logging.debug("Sign in {}".format(points[0]))

    def treasure_hunt(self):
        if self.wait_for_vision_find(self.treasure_hunt_vision):
            points = self.treasure_hunt_vision.find(self.screenshot, 0.9)
            self.move_and_click(points[0])
            logging.debug("Treasure Hunt {}".format(points[0]))

    def next_map(self):
        points = self.next_map_vision.find(self.screenshot, 0.9)
        if points:
            self.move_and_click(points[0])
            logging.debug("Next Map {}".format(points[0]))

    def put_heroes_to_work(self):
        for i in range(3):
            logging.debug("Work {}".format(i))
            if self.wait_for_vision_find(self.work_vision):
                points = self.work_vision.find(self.screenshot, 0.85)
                for point in points:
                    self.move_and_click(point)
                    self.move_and_click(point)
                    sleep(1)
                if i < 2:
                    pyautogui.drag(0, -350, 0.5, button='left')
                    sleep(0.5)

    def refresh_heroes(self):
        self.refresh_time = time()
        points = self.back_vision.find(self.screenshot, 0.9)
        self.move_and_click(points[0])
        logging.debug("Back {}".format(points[0]))
        if self.wait_for_vision_find(self.heroes_vision):
            points = self.heroes_vision.find(self.screenshot, 0.9)
            self.move_and_click(points[0])
            logging.debug("Heroes {}".format(points[0]))
            self.put_heroes_to_work()
            if self.wait_for_vision_find(self.exit_vision):
                points = self.exit_vision.find(self.screenshot, 0.9)
                self.move_and_click(points[0])
                logging.debug("Exit {}".format(points[0]))
                self.treasure_hunt()

    def start(self):
        self.stopped = False
        main_thread = Thread(target=self.run)
        checker_thread = Thread(target=self.run_checkers)
        main_thread.start()
        checker_thread.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            sleep(0.05)
            if self.screenshot is not None:
                if self.state == BotState.INITIALIZING:
                    self.change_state(BotState.SEARCHING)
                elif self.state == BotState.SEARCHING:
                    self.search()
                elif self.state == BotState.REFRESH_HEROES:
                    self.refresh_heroes()
                    self.change_state(BotState.SEARCHING)
                elif self.state == BotState.ERROR:
                    self.error()
                    self.change_state(BotState.SEARCHING)
                elif self.state == BotState.CONNECT_WALLET:
                    self.connect_wallet()
                    self.change_state(BotState.SIGN_IN)
                # elif self.state == BotState.SELECT_WALLET:
                #     self.select_wallet()
                #     self.change_state(BotState.SIGN_IN)
                elif self.state == BotState.SIGN_IN:
                    self.sign_in()
                    self.change_state(BotState.TREASURE_HUNT)
                elif self.state == BotState.TREASURE_HUNT:
                    self.treasure_hunt()
                    self.change_state(BotState.SEARCHING)
                elif self.state == BotState.NEXT_MAP:
                    self.next_map()
                    self.change_state(BotState.SEARCHING)

    def run_checkers(self):
        while not self.stopped:
            if self.screenshot is not None:
                self.check_error()
                self.check_loading_page()
                sleep(0.05)
