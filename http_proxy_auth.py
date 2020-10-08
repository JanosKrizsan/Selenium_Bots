import os
import zipfile
from selenium import webdriver

def create_manifest_json():

    return """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

def create_background_js(proxy_full):
    proxy = proxy_full.split(":")
    host = proxy[0]
    port = proxy[1]
    user = proxy[2]
    pwd = proxy[3]

    return """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (host, port, user, pwd)


def get_chromedriver(driver_path, use_proxy=False, user_agent=None, proxy=None):
    path = driver_path
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        manifest_json = create_manifest_json()
        background_js = create_background_js(proxy)
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        os.path.join(path, 'chromedriver'),
        chrome_options=chrome_options)
    return driver

#driver = get_chromedriver(use_proxy=True)
#driver.get('https://www.google.com/search?q=my+ip+address')
#driver.get('https://httpbin.org/ip')

#Source -> https://stackoverflow.com/questions/55582136/how-to-set-proxy-with-authentication-in-selenium-chromedriver-python