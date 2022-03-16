from queue import Empty
from urllib import request
from matplotlib import image
from numpy import array, histogram
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
import math
import operator
from functools import reduce

username = 'k22616416'
password = 'kk013579'

url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/'
imageSavePath = 'files'

MUSIC_LEVEL_IMAGE_PATHS = {
    "BASIC": "/asset/level/diff_basic.png",
    "ADVANCED": "\\asset\\level\\diff_advanced.png",
    "EXPERT": "\\asset\\level\\diff_expert.png",
    "MASTER": "\\asset\\level\\diff_master.png"
}

MUSIC_TYPE_IMAGE_PATHS = {
    "DX": "\\asset\\type\\music_dx.png",
    "でらっくす": "\\asset\\type\\music_standard.png"
}


# class MusicLevels(Enum):
#     BASIC = 0
#     ADCANCED = 1
#     EXPERT = 2
#     MASTER = 3


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


def CompareImages(pic1: image, pic2: image) -> bool:
    histogram1 = pic1.histogram()
    histogram2 = pic2.histogram()
    differ = math.sqrt(reduce(operator.add, list(
        map(lambda a, b: (a-b)**2, histogram1, histogram2)))/len(histogram1))
    return (differ == 0)


def LevelClassification(imgUrl) -> str:
    for i in MUSIC_LEVEL_IMAGE_PATHS:
        if CompareImages(Image.open(os.getcwd() + MUSIC_LEVEL_IMAGE_PATHS[i]), Image.open(requests.get(imgUrl, stream=True).raw)):
            return i


def MusicTypefication(imgUrl) -> str:
    for i in MUSIC_TYPE_IMAGE_PATHS:
        if CompareImages(Image.open(os.getcwd() + MUSIC_TYPE_IMAGE_PATHS[i]), Image.open(requests.get(imgUrl, stream=True).raw)):
            return i


def GetNewPhotos():
    chrome.get("https://maimaidx-eng.com/maimai-mobile/photo/")
    WebDriverWait(chrome, 20).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.m_10.p_5.f_0')))
    photoFrames = chrome.find_elements_by_css_selector('.m_10.p_5.f_0')

    print(len(photoFrames))
    count = 0
    mainWindow = chrome.current_window_handle
    for frame in photoFrames:
        WebDriverWait(chrome, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.block_info.p_3.f_11.white')))
        dateTag = frame.find_element_by_css_selector(
            '.block_info.p_3.f_11.white')
        date = dateTag.text
        if date == None:
            print('Date empty')
            continue

        # 抓歌名
        songName = frame.find_element_by_css_selector(
            '.black_block.w_430.m_3.m_b_5.p_5.t_l.f_15.break').text

        # 抓圖片Url
        photoTag = frame.find_elements_by_css_selector('.w_430')[1]
        imgurl = photoTag.get_attribute("src")

        # 抓難度
        levelUrl = frame.find_element_by_css_selector(
            '.h_16.f_l').get_attribute("src")
        level = LevelClassification(levelUrl)

        # 抓類型
        musicTypeUrl = frame.find_element_by_css_selector(
            '.music_kind_icon.f_r').get_attribute("src")
        musicType = MusicTypefication(musicTypeUrl)

        # 開新分頁存圖
        chrome.execute_script("window.open('"+imgurl+"');")
        chrome.switch_to_window(
            chrome.window_handles[len(chrome.window_handles)-1])

        dirPath = os.path.join(imageSavePath, (date.split(' '))[
            0].replace('/', ''))

        # 檢查資料夾路徑
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
            print("Make new dir : " + dirPath)

        # 去掉日期中的/跟:
        imgName = os.path.join(
            dirPath, (date.replace('/', '')).replace(':', '.') + ' ' + songName + " " + level + '(' + musicType + ').png')

        # 檢查是否已存在
        if not os.path.isfile(imgName):
            # 不存在就存檔
            WebDriverWait(chrome, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH, "/html/body/img")))
            with open(imgName, 'wb') as file:
                file.write(chrome.find_element_by_xpath(
                    "/html/body/img").screenshot_as_png)
            print("Save : " + imgName)

        chrome.close()
        chrome.switch_to_window(mainWindow)
        count += 1


def main():

    Login_maimai_net()
    GetNewPhotos()


if __name__ == '__main__':
    main()
