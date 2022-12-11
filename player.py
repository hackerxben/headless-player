import time
from selenium import *
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import signal
import sys
import pathlib

def create_driver():
    chrome_options= webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('--start-maximized')
    current_dir = pathlib.Path(__file__).parent.resolve()
    chrome_options.add_extension(str(current_dir)+'/AdBlock.crx')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)
    driver.get("chrome://extensions/?id=gighmmpiobklfepjocnamgkkbiglidom") 
    # select allow in incognito mode checkbox
    driver.execute_script("document.querySelector(\"body > extensions-manager\").shadowRoot.querySelector(\"#viewManager > extensions-detail-view\").shadowRoot.querySelector(\"#allow-incognito\").shadowRoot.querySelector(\"#crToggle\").click()")
    return driver

driver = create_driver()

def play(driver:WebDriver,url):
    driver.get(url)
    if "youtube" in url:
        driver.find_element(By.CSS_SELECTOR,"#movie_player > div.ytp-cued-thumbnail-overlay > button").click()
        video_title = driver.find_element(By.CSS_SELECTOR,"#title > h1 > yt-formatted-string").text
        print("Current video: "+video_title)
        while(video_title):
            try:
                find_yes_btn = driver.find_element(By.CSS_SELECTOR,"#button")
                if(find_yes_btn):
                    find_yes_btn.click()
            except Exception:
                "No confirm button"
            new_video_title = driver.find_element(By.CSS_SELECTOR,"#title > h1 > yt-formatted-string").text
            if(new_video_title != video_title):
                video_title = new_video_title
                print("Current video: "+video_title)
            time.sleep(3)
    else:
        print(driver.title)
        driver.find_element(By.CSS_SELECTOR,"#jw6 > div.jw-wrapper.jw-reset > div.jw-controls.jw-reset > div.jw-controlbar.jw-reset > div > div.jw-icon.jw-icon-inline.jw-button-color.jw-reset.jw-icon-playback").click() 

def signal_handler(sig, frame):
    try:
        driver.close()
    except Exception:
        print("See you next time")
    sys.exit(0)

if __name__ == "__main__":
    if sys.argv[1]:
        url = sys.argv[1]
    try:
        signal.signal(signal.SIGINT, signal_handler)
        print('Press Ctrl+C to exit')
        play(driver,url)
        signal.pause()
    except Exception as error:
        print("going to close chrome")
        driver.close()
        print(error)