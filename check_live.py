from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# TARGET_URL = "https://5721004.xyz/player/pandalive.html?url=pandaclass"  
TARGET_URL = "https://5721004.xyz/player/pandalive.html?url=sexymin12"
PROXY = "http://127.0.0.1:7890"  

def check_is_live():
    opts = Options()
    opts.add_argument("--headless=new") 
    opts.add_argument("--no-sandbox")
    #opts.add_argument(f"--proxy-server={PROXY}")
    opts.add_argument("--disable-dev-shm-usage") 
    opts.add_argument("--disable-gpu")   
    opts.add_argument("--window-size=1920,1080")  
    opts.add_experimental_option("excludeSwitches", ["enable-logging"]) 

    #service = Service(executable_path=r"D:\code\recoder\chromedriver.exe")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=opts)
    driver.get(TARGET_URL)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    is_live = bool(soup.find("div", string="获取失败，错误信息：castEnd"))

    print(not is_live)
    
    driver.quit() 

if __name__ == '__main__':
    check_is_live()