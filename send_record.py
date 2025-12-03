import time
import os
from selenium.webdriver.common.by import By

TARGET_URL = os.getenv("RECORD_URL")

def send_record(driver,userid,url,tgid):
    driver.get(TARGET_URL)
    time.sleep(5)

    input_userid = driver.find_element(By.ID,"userid")
    input_userid.clear()
    input_userid.send_keys(userid)

    input_url = driver.find_element(By.ID,"url")
    input_url.clear()
    input_url.send_keys(url)
    
    input_tgid = driver.find_element(By.ID,"tgid")
    input_tgid.clear()
    input_tgid.send_keys(tgid)

    submit_btn = driver.find_element(By.XPATH, "//input[@type='submit' and @value='提交']")
    submit_btn.click()
    
    driver.quit() 
