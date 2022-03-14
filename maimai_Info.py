from queue import Empty
from urllib import request
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
from io import StringIO
import os
import urllib.request


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
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.m_10.p_5.f_0')))
    # photoFrames = chrome.find_elements_by_xpath('/html/body/div[2]/div[2]')
    photoFrames = chrome.find_elements_by_css_selector('.m_10.p_5.f_0')

    print(len(photoFrames))
    count = 0
    for frame in photoFrames:
        # photo = frame.find_element_by_xpath(
        #     '/html/body/div[2]/div[2]/div/img[3]')
        WebDriverWait(chrome, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.block_info.p_3.f_11.white')))
        dateTag = frame.find_element_by_css_selector(
            '.block_info.p_3.f_11.white')
        date = dateTag.text
        if date == None:
            print('Date empty')
            continue

        # 3/14 photo css需要修改
        photo = frame.find_element_by_css_selector('.w_430')
        imgurl = photo.get_attribute("src")
        chrome.get(imgurl)

        with open(date+'.png', 'wb') as file:
            file.write(chrome.find_element_by_xpath(
                "/html/body/img").screenshot_as_png)
        count += 1


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
