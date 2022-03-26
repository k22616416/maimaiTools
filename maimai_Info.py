from http import client
from multiprocessing.connection import wait


import discord
from discord.ext import tasks, commands

from queue import Empty
from urllib import request
from matplotlib import image
from numpy import array, empty, histogram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions
# from pandas.core.frame import DataFrame
from enum import Enum
from PIL import Image
import requests
# from io import StringIO
import os
# import urllib.request
import math
import operator
from functools import reduce
import threading
import json
import time
import queue
import datetime

global userCollection

# usernameCollection = ['k22616416']
# passwordCollection = ['kk013579']
NOT_IN_SERVICE_START_TIME = datetime.datetime.strptime('03:00:00', "%H:%M:%S")
NOT_IN_SERVICE_END_TIME = datetime.datetime.strptime('06:00:00', "%H:%M:%S")

url = 'https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/'
imageSavePath = 'files'

DISCORD_BOT_TOKEN = ''

MUSIC_LEVEL_IMAGE_PATHS = {
    "BASIC": "\\asset\\level\\diff_basic.png",
    "ADVANCED": "\\asset\\level\\diff_advanced.png",
    "EXPERT": "\\asset\\level\\diff_expert.png",
    "MASTER": "\\asset\\level\\diff_master.png",
    "REMASTER": "\\asset\\level\\diff_remaster.png"
}

MUSIC_TYPE_IMAGE_PATHS = {
    "DX": "\\asset\\type\\music_dx.png",
    "でらっくす": "\\asset\\type\\music_standard.png"
}

SAVE_JSON_PATHS = '/files/AutoSaveList.json'

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
options.add_argument("--headless")

options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])


# class MyCog(commands.Cog):
#     def __init__(self, bot):
#         self.index = 0
#         self.bot = bot
#         self.printer.start()

#     def cog_unload(self):
#         self.printer.cancel()

#     @tasks.loop(seconds=5.0)
#     async def printer(self):
#         print(self.index)
#         self.index += 1

#     @printer.before_loop
#     async def before_printer(self):
#         print('waiting...')
#         await self.bot.wait_until_ready()


def Login_maimai_net(chrome: webdriver, username: str, password: str):

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


def GetNewPhotos(chrome: webdriver, username: str):

    chrome.get("https://maimaidx-eng.com/maimai-mobile/photo/")
    try:
        WebDriverWait(chrome, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.m_10.p_5.f_0')))
    except exceptions.TimeoutException as exception:
        print('登入失敗，伺服器維修或帳號密碼有誤')
        return []

    photoFrames = chrome.find_elements_by_css_selector('.m_10.p_5.f_0')

    mainWindow = chrome.current_window_handle
    NewPhotosCollection = []
    for frame in photoFrames:
        try:
            WebDriverWait(chrome, 20).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.block_info.p_3.f_11.white')))
        except exceptions.TimeoutException as exception:
            continue
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

        dirPath = os.path.join(imageSavePath, username, (date.split(' '))[
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
            try:
                WebDriverWait(chrome, 20).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "/html/body/img")))
            except exceptions.TimeoutException as exception:
                continue
            with open(imgName, 'wb') as file:
                file.write(chrome.find_element_by_xpath(
                    "/html/body/img").screenshot_as_png)
            print("Save : " + imgName)
            NewPhotosCollection.append(imgName)

        chrome.close()
        chrome.switch_to_window(mainWindow)

    return NewPhotosCollection


def SetAutoSaveUser(author: str, username: str, passwd: str):
    fileName = os.path.join(os.getcwd() + SAVE_JSON_PATHS)
    file = open(fileName, "r+")
    try:
        with file as f:
            data = json.load(f)
    except:
        return 1

    file.close()
    jsonString = '{\
        "discordID": "'+author.replace("'", "\\'").replace('"', '\\"') + '",\
        "valuse": {\
            "username": "'+username.replace("'", "\\'").replace('"', '\\"')+'",\
            "password": "'+passwd.replace("'", "\\'").replace('"', '\\"')+'"\
    }}'
    # jsonString = '{"'+author+'": {"username": "' +
    # username+'","password": "'+passwd+'"}}'
    jsonString = json.loads(jsonString)

    for users in userCollection:
        if username == users.get('valuse').get('username'):
            return 2

    # for i in data:
    #     if i == jsonString:
    #         return 2

    data.append(jsonString)

    file = open(fileName, "w+")
    json.dump(data, file)
    file.close()
    return 0


def GetUserList():
    global userCollection
    fileName = os.path.join(os.getcwd() + SAVE_JSON_PATHS)
    file = open(fileName, "r+")
    try:
        with file as f:
            userCollection = json.load(f)
    except:
        return 1

    file.close()
    return 0


client = discord.Client()
# 調用event函式庫


@ client.event
# 當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    # user = await client.fetch_user(user_id=378159148862275584)
    # await user.send('start bot')
    GetNewPhotosTask.start()


@ client.event
# 當有訊息時
async def on_message(message):
    # 排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return

    if message.content.startswith('.uwu'):
        # 分割訊息成兩份
        tmp = message.content.split(" ")
        # 如果分割後串列長度只有1
        if len(tmp) == 1:
            await message.channel.send("蛤?")
        elif tmp[1] == 'maimai':
            if tmp[2] == '自動存圖':
                if message.channel.type != discord.ChannelType.private:
                    await message.channel.send("<@"+str(message.author.id) + "> 私")
                    await message.author.send('在這裡講會比較安全')
                    await message.author.send('請按照格式輸入:')
                    await message.author.send('```.uwu maimai 自動存圖 "帳號" "密碼"(不含"符號)```')
                    return
                if len(tmp) != 5:
                    await message.author.send('指令錯誤，正確格式為:')
                    await message.author.send('```.uwu maimai 自動存圖 "帳號" "密碼"(不含"符號)```')
                    return

                # 去掉帳號密碼頭尾的引號
                tmp[3] = tmp[3].strip("\'")
                tmp[3] = tmp[3].strip("\"")
                tmp[4] = tmp[4].strip("\'")
                tmp[4] = tmp[4].strip("\"")

                # 儲存自動存圖的maimai net帳密
                err = SetAutoSaveUser(str(message.author.id), tmp[3], tmp[4])
                if err == 1:
                    await message.author.send('機器人檔案錯誤，請聯絡可愛的蝦蝦')
                    return
                elif err == 2:
                    await message.author.send('此帳號已設定自動存圖')
                    return
                elif err == 0:
                    await message.author.send('已設定自動存圖，最慢10分鐘後你會看到圖片uwu')

                    return
        elif tmp[1] == 'userid':
            await message.author.send(message.author)
        else:
            await message.channel.send(tmp[1])

    elif message.content.startswith('ping'):
        await message.channel.send("pong")

global PhotoTaskBusyFlag
PhotoTaskBusyFlag = False


@ tasks.loop(minutes=10)
async def GetNewPhotosTask():
    global PhotoTaskBusyFlag
    if datetime.datetime.now().time() > NOT_IN_SERVICE_START_TIME.time() and datetime.datetime.now().time() < NOT_IN_SERVICE_END_TIME.time():
        print('maimai net維修')
        return
    if PhotoTaskBusyFlag:
        return
    if GetUserList() != 0:
        print("GetUserList error")
        return
    for users in userCollection:

        user_tmp = users.get('valuse').get('username')
        pawd_tmp = users.get('valuse').get('password')
        userDcId = users.get('discordID')
        PhotoTaskBusyFlag = True

        chrome = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        chrome.get(url)
        Login_maimai_net(chrome, user_tmp, pawd_tmp)

        # 抓使用者
        user = await client.fetch_user(user_id=int(userDcId))
        print("正在確認"+user.display_name+"的新照片")
        photoFiles = GetNewPhotos(chrome, userDcId)

        if len(photoFiles) != 0:

            # 機器人傳送圖片
            for image in photoFiles:
                await user.send(file=discord.File(image))
                print('正在傳送新照片給' + user.display_name + ':'+image)
                time.sleep(1)
        print('確認結束')
        chrome.close()

    PhotoTaskBusyFlag = False


client.run(DISCORD_BOT_TOKEN)


# def main():
#     chrome = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
#     chrome.get(url)
#     Login_maimai_net(chrome, usernameCollection[0], passwordCollection[0])
#     GetNewPhotos(chrome, usernameCollection[0])
