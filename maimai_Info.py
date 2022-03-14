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
from enum import Enum
from PIL import Image
import requests

username = 'k22616416'
password = 'kk013579'

url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/'


options = Options()
options.add_argument("--disable-notifications")
options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])

chrome = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
chrome.get(url)


def Login_maimai_net():

    # click SEGA ID button
    WebDriverWait(chrome, 20).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dt/ul/li/span')))
    chrome.find_element_by_xpath(
        '/html/body/div[2]/div[2]/main/article/section[2]/dl/dt/ul/li/span').click()

    # insert username and password
    WebDriverWait(chrome, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[1]/div[2]/input')))
    chrome.find_element_by_xpath(
        '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[1]/div[2]/input').send_keys(username)
    WebDriverWait(chrome, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[2]/div[2]/input')))
    chrome.find_element_by_xpath(
        '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[2]/div[2]/input').send_keys(password)
    WebDriverWait(chrome, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/div/input')))

    # click login button
    chrome.find_element_by_xpath(
        '/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/div/input').click()


def GetNewPhotos():

    chrome.get("https://maimaidx-eng.com/maimai-mobile/photo/")
    WebDriverWait(chrome, 20).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]')))
    photoFrames = chrome.find_elements_by_xpath('/html/body/div[2]/div[2]')
    print(len(photoFrames))
    for frame in photoFrames:
        photo = frame.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/img[3]')

        imgurl = photo.get_attribute("src")
        img_data = requests.get(imgurl).content
        with open('./image_name.jpg', 'wb') as handler:
            handler.write(img_data)


def main():
    Login_maimai_net()
    GetNewPhotos()


if __name__ == '__main__':
    main()


class WorkStatus(Enum):
    Home = 1
    PlayData = 2
    Friends = 3
    Photos = 4
    Records = 5
    Event = 6
    Collection = 7
    Ranking = 8
    Settings = 9
