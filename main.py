from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import argparse
import pickle
from cookieBot import CookieBot

parser = argparse.ArgumentParser(description="Modifies program setup for best performance.")
parser.add_argument("--chromedriver_path", type=str, default="C:\chromedriver.exe", help="Defines chromedriver.exe path.")
parser.add_argument("--clicks_to_upgrade", type=int, default=10, help="Defines number of clicks between next upgrade phase.")
parser.add_argument("--time_for_page_loading", type=int, default=2, help="Defines time before program start running.")

args = parser.parse_args()

# Window Setup
bot = CookieBot()
bot.settings.chromedriver_path = args.chromedriver_path
bot.settings.clicks_to_upgrade = args.clicks_to_upgrade
bot.settings.time_for_page_loading = args.time_for_page_loading
bot.start()