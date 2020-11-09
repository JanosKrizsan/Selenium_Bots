from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from math import floor
from random import randint, random
from http_proxy_auth import get_auth_driver
from http_proxy_nonauth import get_nonauth_driver
from math import floor
#region Helper_Functions

def driver_fail(msg):
	driver.close()
	print(msg)

def find_by_path(parent, path):
	return parent.find_element_by_xpath(path)

def get_daily_invs(parent):
	a_to_a_sec = find_by_path(parent, '//*[contains(@class, "a2a_section")]')
	total_requests = int(find_by_path(a_to_a_sec, '//*[contains(@id, "total_request_count")]').text)
	try:
		daily_requests_done = int(find_by_path(a_to_a_sec, '//*[contains(@id, "daily_request_count")]').text)
		if daily_requests_done >= 25:
			return False
		else:
			return True
	except NoSuchElementException:
		return True

def get_answer_count(parent):
	ans_count = int(find_by_path(parent, '//*[contains(@id, "create_modal_link")]/span[5]').text[:2])
	return ans_count < 3

def wait_certain(time_to_wait):
	driver.implicitly_wait(time_to_wait)

def wait(floor, ceiling):
	driver.implicitly_wait(randint(floor, ceiling))

def go_to_partners_page():
	find_by_path(driver, "//*[@id='root']/div/div/div[2]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div[2]").click()
	wait_certain(4)
	find_by_path(driver, "//*[@id='POPOVER1']/div/div[2]/a[1]/div/div/div[2]/div/div").click()
	wait_certain(4)

def sort(questions):
	q_links, q_answers = [], []
	for question in questions:
		if get_daily_invs(question) and get_answer_count(question):
			link = find_by_path(question, "//*[contains(@id, '_link')]").get_attribute("href").text
			answers = get_answer_count(question)
			q_links.append(link)
			q_answer.append(answers)

	return dict(zip(q_links, q_answers))

def check_proxy():
	driver.get('https://httpbin.org/ip')
	current_ip = driver.find_element_by_tag_name("body").text.split('"')[3]
	proxy_ip = proxy.split(":")[0]
	return proxy_ip == current_ip

def create_proxified_driver(path):
	global proxy
	proxy = input("Add your proxy to connect to.\n").split(":")
	return get_nonauth_driver(path, proxy) if len(proxy.split(":")) == 2 else get_auth_driver(path, False, proxy)

def type_login(field, text):
	for char in text:
		field.send_keys(char)

#endregion

#region Main_Functions

def login():
	email = input("Provide your username.")
	password = input("Provide your password.")

	details = [email, password]

	login_elems = driver.find_elements_by_class_name("header_login_text_box")
	login_btn = "/html/body/div[3]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div/form/div[2]/div[3]/input"
	
	if login_elems == []:
		email = driver.find_element_by_xpath("//*[@id='email']")
		pwd = driver.find_element_by_xpath("//*[@id='password']")
		login_btn = "//*[@id='root']/div/div/div/div/div/div/div[2]/div[2]/div[4]/button"
		login_elems = [email, pwd]
		
	login_pairs = zip(login_elems, details)
	for el, text in login_pairs:
		type_login(el, text)

	if WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotInteractableException]).until(EC.presence_of_element_located((By.XPATH, login_btn))):
		driver.find_element_by_xpath(login_btn).click()
		return True
	return False


def setup():

	path = input("Path to Chrome webdriver:\n")
	q_to_rev = int(input("How many questions should we review?\n"))

	global driver

	driver = create_proxified_driver(path)
	if not check_proxy():
		driver_fail("Proxy did not match IP.")	

	driver.get("https://www.quora.com")

	if login():
		wait_certain(6)
		go_to_partners_page()
		return q_to_rev
	else:
		driver_fail("Could not log in.")

def get_questions(q_to_rev):
	goal = floor(q_to_rev / 2)
	for count in range(goal):
		WebDriverWait(driver, 20).until(lambda d: d.find_element_by_tag_name("body"))
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		wait_certain(5)

	questions = driver.find_elements_by_class_name("card_inner")
	return sort(questions)

def do_actions(req_btn):
	actions = ActionChains(driver)
	req_btn.click()
	invite_btns = driver.find_elements_by_tag_name("circle")
	text_tags = driver.find_elements_by_class_name("q-text")
	sugg_writers = int([i for i in text_tags if "Suggested Writers" in i.text][0][17:19].sub('^[0-9]','','/'))

	for button in invite_btns:
		if sugg_writers < 25:
			wait(3, 5)
			actions.click(button)

def invite(sorted_items):
	for question in sorted_items:
		driver.find_element_by_tag_name("body").send_keys(Keys.LEFT_CONTROL + 't')
		driver.get(question.text)
		wait(3, 5)
		buttons = driver.find_elements_by_class_name("q-text")
		req_button = [i for i in items if i.text == "Request"][0]

		do_actions(req_button)
		driver.find_elements_by_tag_name("body").send_keys(Keys.LEFT_CONTROL + 'w')
	driver.close()

#endregion

if __name__ == "__main__":
	invite(get_questions(setup()))