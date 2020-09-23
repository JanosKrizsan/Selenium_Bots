from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from math import floor
from random import randint, random
import re

#region Helper_Functions

def find(parent, class_name):
	return parent.find_element_by_class_name(class_name)

def get_daily_invs(parent):
	return int(parent.find_element(By.css("[id$=daily_request_count")).text)

def get_answer_count(parent):
	return find(parent, "answer_count").text[:2]

def wait(ceiling):
	driver.implicitly_wait(randint(0, ceiling))

def assign_driver(path):
	if "chrome" in path:
		return webdriver.Chrome(path)
	elif "fox" in path:
		return webdriver.Firefox(path)
	else:
		return webdriver.Opera(path)

def sort(questions):
	q_links, q_answers = [], []
	for question in questions:
		if get_daily_invs(question) < 25 and get_answer_count(question) < 3:
			q_links.append(find(question, "question_link").get_attribute("href"))
			q_answer.append(get_answer_count(question))
	return dict(zip(q_links, q_answers))

#endregion

#region Main_Functions
def setup():

	path = input("Path to Chrome webdriver:\n")
	q_to_rev = int(input("How many questions should we review?\n"))

	global driver
	driver = assign_driver(path)
	driver.get("https://www.quora.com/partners")

	return q_to_rev

def get_questions(q_to_rev):

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
			wait(1)
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
	invite(get_questions())