from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from settings import Settings
from statistics import Statistics
from cookieClicker import CookieClicker
import time

class CookieBot:
    def __init__(self):
        self.settings = Settings()
        self.statistics = Statistics()
        self.url = "https://orteil.dashnet.org/cookieclicker/"
        self.window = None
        self.cookieClicker = CookieClicker()

    def create_window(self):
        self.window = webdriver.Chrome(self.settings.chromedriver_path)

    def go_to_page(self):
        self.window.get(self.url)

    def start(self):
        self.create_window()
        self.go_to_page()
        time.sleep(self.settings.time_for_page_loading)
        self.setup_cookie_clicker()  
        self.run_main_loop()
    
    def setup_cookie_clicker(self):
        self.cookieClicker.cookie_button = self.window.find_element_by_xpath("/html/body/div/div[2]/div[15]/div[8]/div[1]")
        self.cookieClicker.all_elements_in_item_path = self.window.find_elements_by_xpath("/html/body/div/div[2]/div[19]/div[3]/div[6]/*")
        self.cookieClicker.first_upgrade_path = "/html/body/div/div[2]/div[19]/div[3]/div[5]/div[1]"
        self.cookieClicker.upgrades_to_buy = []
        self.cookieClicker.items_to_buy = [item for item in self.cookieClicker.all_elements_in_item_path if
                item.get_attribute("class") == "product locked disabled" or "product locked disabled toggledOff"]

    def check_upgrades(self):
        try:
            upgrade = self.window.find_element_by_xpath(self.cookieClicker.first_upgrade_path)
            if upgrade.get_attribute("class") == "crate upgrade enabled":
                upgrade.click()
                return True
        except NoSuchElementException:
            pass
        return False

    def check_items_to_buy(self):
        next_check = False
        items_ready_to_buy = []
        for item in self.cookieClicker.items_to_buy:
            if item.get_attribute("class") == "product unlocked enabled":
                items_ready_to_buy.append(item)
        if items_ready_to_buy:
            items_ready_to_buy.reverse()
            items_ready_to_buy[0].click()
            next_check = True
            time.sleep(self.settings.buy_delay)
        if next_check:
            self.check_items_to_buy()

    def run_main_loop(self):
        clicks_done = 0
        upgrade_attempt = 0
        while 1:
            self.cookieClicker.cookie_button.click()
            clicks_done += 1
            if clicks_done >= self.settings.clicks_to_upgrade:
                
                print(str(clicks_done) + " " + str(upgrade_attempt))
                if self.check_upgrades():
                    self.check_items_to_buy()
                else:
                    upgrade_attempt += 1

                if upgrade_attempt == self.settings.upgarde_attempts_before_items:
                    self.check_items_to_buy()
                    upgrade_attempt = 0
                clicks_done = 0

