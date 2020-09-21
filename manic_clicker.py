from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def actions(driver, ID, clicks):
	actions = ActionChains(driver)
	actions.double_click(driver.find_element_by_id(ID))
	for i in range(clicks):
		actions.perform()

def run_me():

	PATH = input("Provide the full path of the webdriver, Chrome or Firefox:\n")
	LINK = input("Provide the link to the website you want clicks on:\n")
	ID = input("Provide the ID of the item you want clicked like a maniac:\n")
	DBL_CLICKS = int(input("How many double clicks do you want?:\n"))

	if "chrome" in PATH:
		driver = webdriver.Chrome(PATH)
	else:
		driver = webdriver.Firefox(PATH)

	driver.get(LINK)
	driver.implicitly_wait(5)

	actions(driver, ID, DBL_CLICKS)

	while True:
		decision = input("Provde a new number or type 'quit' to quit:\n")
		if decision.isdigit():
			actions(driver, ID, int(decision))
		elif decision == "quit":
			driver.close()
		else:
			print("You provided the wrong input, try again.\n")

if __name__ == "__main__":
	run_me()
