import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller

USERNAME = "aanshul22@gmail.com"
PASSWORD = "Xruvix#3400"
URL = "https://in.tradingview.com/"
BUY = "Buy"
SELL = "Sell"

def load_page():
	global URL
	options = webdriver.ChromeOptions()
	# options.add_argument("headless")
	options.binary_location = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"
	browser = webdriver.Chrome("C:/Chromium Driver/chromedriver.exe", chrome_options=options)
	browser.get(URL)
	return browser


def login():
	global browser
	element = browser.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[3]/button[1]")
	element.click()

	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "item-2IihgTnv"))
		)
	finally:
		element = browser.find_element_by_class_name("item-2IihgTnv")
		element.click()

	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "js-show-email"))
		)
	finally:
		element = browser.find_element_by_class_name("js-show-email")
		element.click()

	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.NAME, "username"))
		)
	finally:
		element = browser.find_element_by_name("username")
		element.send_keys(USERNAME)

	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.NAME, "password"))
		)
	finally:
		element = browser.find_element_by_name("password")
		element.send_keys(PASSWORD)

	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "tv-button--loader"))
		)
	finally:
		element = browser.find_element_by_class_name("tv-button--loader")
		element.click()

	input("Press Any Key To Continue (login)... ")
	time.sleep(3)

	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "button-DABaJZo4"))
		)
	finally:
		element_1 = browser.find_elements_by_class_name("button-DABaJZo4")[0]
		element_2 = browser.find_element_by_class_name("isActive-DABaJZo4")
		if element_1 != element_2:
			element_1.click()


def get_watchlist():
	#  inner-EJ_LFrif
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "inner-EJ_LFrif"))
		)
	finally:
		element = browser.find_elements_by_class_name("inner-EJ_LFrif")
		# print(len(element))
		watch_list = []
		for e in element[::6]:
			print(e.text)
		watch_list.append(e.text)
		return watch_list


def go_to_chart():
	#  tv-mainmenu__item--chart
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "tv-mainmenu__item--chart"))
		)
	finally:
		element = browser.find_element_by_class_name("tv-mainmenu__item--chart")
		element.click()
		time.sleep(3)


def go_to_next_future():
	#  indicators-EJ_LFrif
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "indicators-EJ_LFrif"))
		)
	finally:
		element = browser.find_elements_by_class_name("indicators-EJ_LFrif")
		print(len(element))
		
		for e in element:
			e.click()
			print(e.text)
			time.sleep(0.5)
			yield 1

		return 0

def create_alert(action):
	global keyboard
	keyboard.press(Key.alt_l)
	keyboard.press('a')
	keyboard.release('a')
	keyboard.release(Key.alt_l)
	time.sleep(0.1)
	#  tv-alert-dialog__group-item--left
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "tv-alert-dialog__group-item--left"))
		)
	finally:
		element = browser.find_elements_by_class_name("tv-alert-dialog__group-item--left")
		element[0].click()

	#  Machine Learning
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located(
				(By.CLASS_NAME, "tv-control-select__option-wrap"))
		)
	finally:
		element = browser.find_elements_by_class_name(
			"tv-control-select__option-wrap")
		
		for e in element:
			if "Machine" in e.text:
				e.click()
				break

	#  Buy/Sell
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located(
				(By.CLASS_NAME, "tv-control-select__wrap"))
		)
	finally:
		element = browser.find_elements_by_class_name(
			"tv-control-select__wrap")
		element[1].click()

	#  tv-control-select__option-wrap
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located(
				(By.CLASS_NAME, "tv-control-select__option-wrap"))
		)
	finally:
		element = browser.find_elements_by_class_name(
			"tv-control-select__option-wrap")
		for e in element:
			if e.text == action:
				e.click()
				break

	# Once per bar close
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located(
				(By.CLASS_NAME, "tv-alert-dialog__button-caption"))
		)
	finally:
		element = browser.find_elements_by_class_name(
			"tv-alert-dialog__button-caption")
		element[2].click()

	#  tv-control-input
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located(
				(By.CLASS_NAME, "tv-control-input"))
		)
	finally:
		element = browser.find_elements_by_class_name(
			"tv-control-input")
		element[1].send_keys("Buy {{ticker}}")

	#  tv-button__loader
	try:
		element = WebDriverWait(browser, 5).until(
			EC.presence_of_element_located(
				(By.CLASS_NAME, "tv-button__loader"))
		)
	finally:
		element = browser.find_elements_by_class_name(
			"tv-button__loader")
		element[0].click()

	pyautogui.click(500, 500)
	

if __name__ == "__main__":
	global browser
	keyboard = Controller()
	browser = load_page()
	browser.maximize_window()
	login()
	# watch_list = get_watchlist()
	go_to_chart()

	input("Press Any Key To Continue... ")
	time.sleep(3)
	start = go_to_next_future()
	while start:
		create_alert(BUY)
		time.sleep(0.25)
		# create_alert(SELL)
		time.sleep(0.25)
		start = go_to_next_future()
	
	
	time.sleep(10)

	browser.quit()
