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
        self.bought_last = False

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
        self.cookieClicker.upgrades_path = "/html/body/div/div[2]/div[19]/div[3]/div[5]/*"
        self.cookieClicker.upgrades_to_buy = []
        self.cookieClicker.items_to_buy = [item for item in self.cookieClicker.all_elements_in_item_path if
                item.get_attribute("class") == "product locked disabled" or "product locked disabled toggledOff"]

    def check_upgrades(self):
        is_upgrade = False
        try:
            upgrades = self.window.find_elements_by_xpath(self.cookieClicker.upgrades_path)
            for upgrade in upgrades:
                if upgrade.get_attribute("class") == "crate upgrade enabled":
                    upgrade.click()
                    is_upgrade = True
        except:
            pass
        return is_upgrade

    def check_items_to_buy(self):
        try:
            next_check = False
            items_ready_to_buy = self.get_shop_items()
            
            if items_ready_to_buy:
                lowest_price = self.get_item_cost(items_ready_to_buy[0])
                lowest_price_item = items_ready_to_buy[0]
                for item in items_ready_to_buy:
                    item_cost = self.get_item_cost(item)
                    if item_cost <= lowest_price:
                        lowest_price_item = item
                        lowest_price = item_cost

                
            if self.statistics.current_item_purchased_amount == self.settings.high_price_item_frequency:
                items_ready_to_buy[0].click()
                cost = self.get_item_cost(items_ready_to_buy[0])
                self.statistics.current_item_purchased_amount = 0
                print("Bought " + self.get_item_name(items_ready_to_buy[0]) + " for " + str(cost))
            else:
                lowest_price_item.click()
                self.statistics.current_item_purchased_amount += 1
                print("Bought " + self.get_item_name(lowest_price_item) + " for " + str(lowest_price))
            
            next_check = True
            time.sleep(self.settings.buy_delay)
            if next_check:
                self.check_items_to_buy()
        except:
            pass

    def run_main_loop(self):
        clicks_done = 0
        upgrade_attempt = 0
        while 1:
            self.cookieClicker.cookie_button.click()
            clicks_done += 1
            if clicks_done >= self.settings.clicks_to_upgrade:
                if self.check_upgrades():
                    self.check_items_to_buy()
                elif len(self.get_upgrades()) < 4:
                    upgrade_attempt += 1

                if upgrade_attempt >= self.settings.upgarde_attempts_before_items:
                    self.check_items_to_buy()
                    upgrade_attempt = 0
                    self.settings.upgarde_attempts_before_items += 1
                clicks_done = 0

    def get_upgrades(self):
        upgrades = []
        try:
            content = self.window.find_elements_by_xpath(self.cookieClicker.upgrades_path)
            for element in content:
                class_name = element.get_attribute("class")
                if class_name == "crate upgrade" or class_name == "crate upgrade enabled":
                    upgrades.append(element)

            return upgrades
        except:
            return upgrades

    def get_shop_items(self):
        items_ready_to_buy = []
        for item in self.cookieClicker.items_to_buy:
            if item.get_attribute("class") == "product unlocked enabled":
                items_ready_to_buy.append(item)

        return items_ready_to_buy

    def get_cookies_amount(self):
        try:
            cookie_number_div = self.window.find_element_by_xpath("/html/body/div/div[2]/div[15]/div[4]")
            cookie_number = cookie_number_div.text
            return self.cost_string_to_int(cookie_number)
        except:
            pass
        return 0

    def get_item_cost(self, WebElement):
        return self.cost_string_to_int(WebElement.find_element_by_class_name("price").text)

    def get_item_name(self, WebElement):
        return WebElement.find_element_by_class_name("title").text

    def cost_string_to_int(self, string):
        fixed_string = ""
        for sign in string:
            if sign == ' ':
                break
            if sign != ',':
                fixed_string += sign
        return int(fixed_string)



