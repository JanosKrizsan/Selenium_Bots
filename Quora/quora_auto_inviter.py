"""Quora Auto-Inviter

This little script logs into your Quora Partner Account via a given proxy (auth or non-auth), scrolls through the list of your
current Questions until it reaches the desired question-count to be viewed. Then, iterating through the questions, opens each,
one by one in a new window, inviting the maximum amount of people to answer to each question. After that it simply closes the 
session.

+ Ends session if IP is not matching your Proxy's IP
+ Retries Login if unsuccessful, asking for details again - or to quit
+ Types username and pass letter by letter

Username -> usually your e-mail address
Password -> well, self-explanatory
Proxy -> IP:PORT:USERNAME:PASSWORD or IP:PORT

TODO:
- Sort questions more efficiently based on given answer count
- Push maximum request numbers based on each question
- Testing

"""
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from math import floor
from random import randint, random
from http_proxy_auth import get_auth_driver
from http_proxy_nonauth import get_nonauth_driver
from time import sleep

#region Helper_Functions

def driver_fail(msg):
	driver.close()
	print(msg)

def find(parent, class_name):
	return parent.find_element_by_class_name(class_name)

def get_daily_invs(parent):
	return int(parent.find_element(By.css("[id$=daily_request_count")).text)

def get_answer_count(parent):
	return find(parent, "answer_count").text[:2]

def wait_certain(seconds):
	sleep(seconds)

def wait(ceiling):
	sleep(randint(0, ceiling))

def sort(questions):
	q_links, q_answers = [], []
	for question in questions:
		if get_daily_invs(question) < 25 and get_answer_count(question) < 3:
			q_links.append(find(question, "question_link").get_attribute("href"))
			q_answer.append(get_answer_count(question))
	return dict(zip(q_links, q_answers))

def check_proxy():
	driver.get('https://httpbin.org/ip')
	current_ip = driver.find_element_by_tag_name("body").text.split('"')[3]
	proxy_ip = proxy.split(":")[0]
	return proxy_ip == current_ip

def create_proxified_driver(path):
	global proxy
	#proxy = input("Add your proxy to connect to.\n").split(":")
	proxy = "" #add your proxy either here or uncomment previous line for direct input, Format => "IP:PORT:USERNAME:PASSWORD"
	return get_nonauth_driver(path, proxy) if len(proxy.split(":")) == 2 else get_auth_driver(path, False, proxy)

def type_login(field, text):
	for char in text:
		wait(1)
		field.send_keys(char)

#endregion

#region Main_Functions

def login():
	#email = input("Provide your username.")
	#password = input("Provide your password.")
	email = "" #replace with your details, or uncomment previous lines for direct input
	password = "" # -""-

	details = [email, password]

	login_elems = driver.find_elements_by_class_name("header_login_text_box")

	login_pairs = zip(login_elems, details)
	for el, text in login_pairs:
		type_login(el, text)

	wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException])
	login_btn = wait.until(driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div[2]/div[4]/button/div"))
	print(wait.text)
	return False;


def setup():

	path = input("Path to Chrome webdriver:\n")
	q_to_rev = int(input("How many questions should we review?\n"))

	global driver

	driver = create_proxified_driver(path)
	if not check_proxy():

		driver_fail("Proxy did not match IP.")	

	driver.get("https://www.quora.com")

	if login():
		driver.get("https://www.quora.com/partners")
		return q_to_rev
	else:
		driver_fail("Could not log in.")

def get_questions(q_to_rev):
	wait_certain(5)
	goal = floor(q_to_rev / 10)
	q_counter = 0
	while q_counter <= goal:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		counter += 1

	questions = driver.find_elements_by_class_name("card_inner")
	return sort(questions)

def do_actions(req_btn):
	actions = ActionChains(driver)
	driver.click(req_btn)
	invite_btns = driver.find_elements_by_tag_name("circle")
	text_tags = driver.find_elements_by_class_name("q-text")
	sugg_writers = int([i for i in text_tags if "Suggested Writers" in i.text][0][17:19].sub('^[0-9]','','/'))

	for button in invite_btns:
		if sugg_writers <= 25:
			wait(3)
			actions.click(button)

def invite(sorted):
	for question in sorted:
		driver.find_element_by_tag_name("body").send_keys(Keys.LEFT_CONTROL + 't')
		driver.get(question.text)
		wait(3)
		buttons = driver.find_elements_by_class_name("q-text")
		req_button = [i for i in items if i.text == "Request"][0]

		do_actions(req_button)
		driver.find_elements_by_tag_name("body").send_keys(Keys.LEFT_CONTROL + 'w')
	driver.close()

#endregion

if __name__ == "__main__":
	invite(get_questions(setup()))