import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import test_database
from send_record import send_record
from selenium.webdriver.common.by import By
from send_to_phone import send_message
import os

def getUserIDs():
    return test_database.getAllStreamer()

USERLiST = getUserIDs()
USERID = USERLiST[0]
TGID = os.getenv("TGID")
LIVE_URL = os.getenv("LIVE_URL")
TARGET_URL = f"{LIVE_URL}{USERID}"
MIN_DELAY = 3  
MAX_DELAY = 8

def startChorme():
    opts = Options()
    opts.add_argument("--headless=new") 
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage") 
    opts.add_argument("--disable-gpu")   
    opts.add_argument("--window-size=1920,1080")  
    opts.add_experimental_option("excludeSwitches", ["enable-logging"]) 

    service = Service(ChromeDriverManager().install())
    #service = Service(executable_path=r"D:\code\recoder\chromedriver.exe")
    driver = webdriver.Chrome(service=service,options=opts)
    return driver

def getLiveState():
    return test_database.getLiveState(USERID)

def check_is_live(driver):
    send_message("--------正在检测直播状态--------",False)
    driver.get(TARGET_URL)
    random_delay()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    is_live = not bool(soup.find("div", string="获取失败，错误信息：castEnd") or soup.find("div", string="获取失败，错误信息：付费房")) 
    pre_is_live = getLiveState()
    if(is_live and is_live != pre_is_live):
        send_message(f"{USERID}开播啦！！！",True)   
    elif(not is_live and is_live != pre_is_live) :
        send_message(f"{USERID}已下播",False)
    elif(not is_live):
        send_message(f"{USERID}未开播",False)
    else :
        send_message(f"{USERID}正在直播中",False)
    return is_live

def updateLiveState(live_state):
    return test_database.updateLiveState(USERID,live_state)

def updateRecordState(record_state):
    return test_database.updateRecordState(USERID,record_state)

def getRecordState():
    return test_database.getRecordState(USERID)

def getRecordPermission():
    return test_database.getRecordPermission(USERID)

def getURL(driver):
    url = driver.find_element(By.ID,"url").get_attribute("value")
    return url

def record(driver):
    send_message("--------正在进行录播检测--------",False)
    record_state = getRecordState()
    record_permission = getRecordPermission()
    if(not record_state and record_permission):
        send_message("--------尝试发起录播--------",False)
        url = getURL(driver)
        try:
            send_record(driver,USERID,url,TGID)
            updateRecordState(True)
            send_message(f"{USERID}成功开启录播",True)
        except:
            send_message(f"{USERID}未能开启录播",True) 
    elif(record_state):
        send_message(f"{USERID}已在录制中",False)
    else:
        send_message(f"{USERID}无录制权限",False)

def send_msg(msg,needSend):
    print(msg)
    if(needSend):
        send_message(msg)

def random_delay(min_sec=MIN_DELAY, max_sec=MAX_DELAY):
    delay = random.uniform(min_sec, max_sec) 
    time.sleep(delay)

def workflow(driver):
    random_delay()
    live_state = check_is_live(driver)
    updateLiveState(live_state)
    if(live_state):
        record(driver)
    random_delay()

if __name__ == '__main__':
    driver = startChorme()
    for i in USERLiST:
        USERID = i
        TARGET_URL = f"{LIVE_URL}{USERID}"
        workflow(driver)
    driver.quit()
