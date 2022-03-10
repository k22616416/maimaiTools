from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.action_chains import ActionChains
from pandas.core.frame import DataFrame

username = 'k22616416'
password = 'kk013579'

url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/'

options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])

chrome = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
chrome.get(url)
WebDriverWait(chrome, 20).until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dt/ul/li/span')))
chrome.find_element_by_xpath(
    '/html/body/div[2]/div[2]/main/article/section[2]/dl/dt/ul/li/span').click()

WebDriverWait(chrome, 20).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[1]/div[2]/input')))
# usernameObj = chrome.find_element_by_id('sid')
usernameObj = chrome.find_element_by_xpath(
    '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[1]/div[2]/input')
print(usernameObj)

usernameObj.send_keys(username)
WebDriverWait(chrome, 20).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[2]/div[2]/input')))
passwordObj = chrome.find_element_by_xpath(
    '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[2]/div[2]/input')
passwordObj.send_keys(password)

WebDriverWait(chrome, 20).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/div/input')))

chrome.find_element_by_xpath(
    '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/div/input').click()
