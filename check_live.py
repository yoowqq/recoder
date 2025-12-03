from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import test_database
from send_record import send_record
from selenium.webdriver.common.by import By

USERID = "yyj01317"
TGID = "7536162543"
TARGET_URL = f"https://5721004.xyz/player/pandalive.html?url={USERID}"

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

 
def check_is_live(driver):
    print("--------正在检测直播状态--------")
    driver.get(TARGET_URL)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    is_live = not bool(soup.find("div", string="获取失败，错误信息：castEnd")) 
    if(is_live):
        print(f"{USERID}已开播")   
    else:
        print(f"{USERID}未开播")
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
    send_record(driver,USERID,url,TGID)

def record(driver):
    print("--------正在进行录播检测--------")
    record_state = getRecordState()
    record_permission = getRecordPermission()
    if(not record_state and record_permission):
        print("--------尝试发起录播--------")
        url = getURL(driver)
        try:
            send_record(driver,USERID,url,TGID)
            updateRecordState(True)
            print("成功开启录播")
        except:
            print("未能开启录播") 
    elif(record_state):
        print(f"{USERID}已在录制中")
    else:
        print(f"{USERID}无录制权限")

def workflow(driver):
    live_state = check_is_live(driver)
    updateLiveState(live_state)
    record(driver)
    time.sleep(2)
    driver.quit()

if __name__ == '__main__':
    driver = startChorme()
    workflow(driver)
