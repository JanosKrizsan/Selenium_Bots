import os
from selenium import webdriver

def get_nonauth_driver(proxy):

	chrome_opt = WebDriverWait.ChromeOptions()
	chrome_opt.add_argument("--proxy-servers=%s" % proxy)

	return webdriver.Chrome(os.path.join(path, 'chromedriver'), chrome_options=chrome_opt)

