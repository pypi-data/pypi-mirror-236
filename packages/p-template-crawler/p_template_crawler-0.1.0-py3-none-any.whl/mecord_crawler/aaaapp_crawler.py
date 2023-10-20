import datetime
import json
import urllib.parse
import time

from lxml import etree
import requests
import json
import os
from mecord_crawler import utils
import logging
import urllib3
import datetime
import shutil
import random
from urllib.parse import *
from PIL import Image
from fake_useragent import UserAgent
import uuid
import calendar
from lxml import etree

COUNTRY_DOMAIN =  {
    "us" : "api.mecordai.com",
    "sg" : "api-sg.mecordai.com",
    "test" : "mecord-beta.2tianxin.com"
}
def domain(country):
    return COUNTRY_DOMAIN[country.lower()]

def downloadDir(curGroupId):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    s = os.path.join(this_dir, ".download", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s

user_id = 0
firstMediaCover = ""
groupCacheConfig = {}
allCount = 0
currentCount = 0
def localFileWithSize(type, path):
    width = 0
    height = 0
    if type == "image":
        img = Image.open(path)
        imgSize = img.size
        width = img.width
        height = img.height
    elif type == "video":
        w, h, bitrate, fps,duration = utils.videoInfo(path, 0)
        width = w
        height = h

    return int(width), int(height)

def pathWithSize(path, w, h):
    if w > 0 and h > 0:
        if "?" in path:
            return f"{path}&width={w}&height={h}"
        else:
            return urljoin(path, f"?width={w}&height={h}")
    return path

def ffmpegGetCover(savePath, tttempPath):
    utils.ffmpegProcess(["-i", savePath, "-ss", "00:00:00.02", "-frames:v", "1", "-y", tttempPath])
    idx=1
    w, h, bitrate, fps,duration = utils.videoInfo(savePath, 0)
    while os.stat(tttempPath).st_size < 3072 and idx < duration and idx < 10:
        utils.ffmpegProcess(["-i", savePath, "-ss", f"00:00:0{idx}.02", "-frames:v", "1", "-y", tttempPath])
        idx+=1
    

def download(country, media_type, post_text, media_resource_url, audio_resource_url, medoa_cover_url, curTaskId):
    name = ''.join(str(uuid.uuid4()).split('-'))
    timeoutDuration = 100
    ext = ".mp4"
    if media_type == "image":
        timeoutDuration = 30
        ext = ".jpg"
    elif media_type == "audio":
        timeoutDuration = 60
        ext = ".mp3"
    savePath = os.path.join(downloadDir(curTaskId), f"{name}{ext}")
    if os.path.exists(savePath):
        os.remove(savePath)
    # download
    logging.info(f"{country} download: {media_resource_url}, {audio_resource_url}")
    s = requests.session()
    s.keep_alive = False
    ua = UserAgent()
    file = s.get(media_resource_url, verify=False, headers={'User-Agent': ua.random}, timeout=timeoutDuration)
    with open(savePath, "wb") as c:
        c.write(file.content)
    # merge audio & video
    if len(audio_resource_url) > 0:
        audioPath = os.path.join(downloadDir(curTaskId), f"{name}.mp3")
        file1 = s.get(audio_resource_url, timeout=timeoutDuration)
        with open(audioPath, "wb") as c:
            c.write(file1.content)
        tmpPath = os.path.join(downloadDir(curTaskId), f"{name}.mp4.mp4")
        utils.ffmpegProcess(["-i", savePath, "-i", audioPath, "-vcodec", "copy", "-acodec", "copy", "-y", tmpPath])
        if os.path.exists(tmpPath):
            os.remove(savePath)
            os.rename(tmpPath, savePath)
            os.remove(audioPath)
        logging.info(f"{country} merge => {file}, {file1}")

    if os.path.exists(savePath) == False or os.stat(savePath).st_size < 10000: #maybe source video is wrong, check output file is large than 20k
        raise Exception("file is too small")
        
    # cover & sourceFile
    coverPath = ""
    if media_type == "video":
        tttempPath = f"{savePath}.jpg"
        if len(medoa_cover_url) > 0:
            s1 = requests.session()
            s1.keep_alive = False
            file1 = s1.get(medoa_cover_url, verify=False, headers={'User-Agent': ua.random}, timeout=timeoutDuration)
            with open(tttempPath, "wb") as c1:
                c1.write(file1.content)
        else:
            # utils.processMoov(savePath,BIN_IDX)
            # utils.ffmpegProcess(["-i", savePath, "-ss", "00:00:00.02", "-frames:v", "1", "-y", tttempPath])
            ffmpegGetCover(savePath, tttempPath)
        if os.path.exists(tttempPath):
            coverPath = tttempPath
    elif media_type == "image":
        coverPath = savePath
    savePathW, savePathH = localFileWithSize(media_type, savePath)
    url = utils.uploadWithDir(country, f"c/n_{curTaskId}", savePath, (media_type == "image"))
    if url == None:
        logging.info(f"{country} oss url not found")
        return
    ossurl = pathWithSize(url, savePathW, savePathH)
    cover_url = ""
    if os.path.exists(coverPath) and media_type == "video":
        cover_url = utils.uploadCoverAndRemoveFile(country, f"c/n_{curTaskId}", coverPath)
        if os.path.exists(coverPath):
            os.remove(coverPath)
    elif os.path.exists(coverPath) and media_type == "image":
        cover_url = ossurl
    s.close()
    if os.path.exists(savePath):
        os.remove(savePath)
    return ossurl, cover_url
    
def updateUser(country, task_id, group_id, url, userConfig):
    global firstMediaCover
    #create
    randomName = ''.join(str(uuid.uuid4()).split('-'))
    coverPathTmp = os.path.join(downloadDir(task_id), f"cover_{randomName}.jpg")
    s = requests.session()
    s.keep_alive = False
    coverOss = ""
    if userConfig["avatar"] != None and len(userConfig["avatar"]) > 0:
        js_res = s.get(userConfig["avatar"], timeout=60)
        with open(coverPathTmp, "wb") as c:
            c.write(js_res.content)
        coverOss = utils.uploadWithDir(country, "cover", coverPathTmp, True)
        os.remove(coverPathTmp)
    elif len(firstMediaCover)>0:
        coverOss = firstMediaCover
    param = {
        "nick_name": userConfig["username"],
        "head_image": coverOss
    }
    s1 = requests.session()
    s1.keep_alive = False
    res = s1.post(f"https://{domain(country)}/proxymsg/crawler/create_user", json.dumps(param), verify=False, timeout=30)
    if res.status_code == 200:
        utils.idlingService(isWorking=True)
        result = json.loads(res.content)
        uid = result["body"]["uid"]
        return uid
    else:
        raise Exception(f"create_user fail!, msg={res}, param={param}")

def mediatype2mecord(media_type):
    if media_type == "image":
        return 1
    elif media_type == "audio":
        return 3
    elif media_type == "video":
        return 2
    return 4
    
def processPosts(country, taskid, group_id, gallery_name, user_type):
    global groupCacheConfig
    if taskid not in groupCacheConfig:
        groupCacheConfig[taskid] = {}

    post_list = []
    for k in groupCacheConfig[taskid]:
        if isinstance(groupCacheConfig[taskid][k], (dict)):
            uuid = groupCacheConfig[taskid][k]
            uuid["group_id"] = group_id
            # if uuid["post"][0]["content_type"] == mediatype2mecord("image"):
            #     if len(uuid["post"]) > 2:#large than 2 pics use template
            #         needTemplate = False#(random.randint(0,5) == 2)
            #         imgTemplate = template_utils.imageTemplate(len(uuid["post"]))
            #         if needTemplate and len(imgTemplate) > 0:
            #             uuid["post"][0]["info"][0] += f"<tid:{imgTemplate}>"
            #         # else:
            #         #     uuid["info"][0] += "<tid:0>"
            #         #     image_gallery["post"].append(uuid)
            # else:
            #     needTemplate = False#(random.randint(0,5) == 2)
            #     videoTemplate = template_utils.videoTemplate(1)
            #     if needTemplate and len(videoTemplate) > 0:
            #         uuid["post"][0]["info"][0] += f"<tid:{videoTemplate}>"
            #     # else:
            #     #     uuid["info"][0] += "<tid:0>"
            #     # normal_gallery["post"].append(uuid)
            post_list.append(uuid)
        groupCacheConfig[taskid][k] = ""

    if len(post_list) == 0:
        #ignore post
        return
    
    for p in post_list:
        param = { "param": [p] } 
        s = requests.session()
        s.keep_alive = False
        s.headers.update({'Connection':'close'})
        res = s.post(f"https://{domain(country)}/proxymsg/crawler/create_post_batch", json.dumps(param), verify=False, timeout=30)
        if res.status_code == 200 and len(res.content) > 0:
            utils.idlingService(isWorking=True)
            logging.info(f"{country} send post success")
            print(f"{country} === publish batch!")
        else:
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"publish_{taskid}.txt"), 'w') as f111:
                json.dump(param, f111)
            logging.info(f"{country} send post fail, res = {res}, param={param}")
            print(f"{country} === publish batch fail~~~")
        time.sleep(0.5)
        
from hashlib import md5
def _translateWithBaidu(text):
    appid = "20191119000358506"
    secretKey = "HOF7aswr7womtU5v6ng6"
    salt = random.randint(32768,65536)
    sign = appid + text + str(salt) + secretKey
    md = md5()
    md.update(sign.encode(encoding='utf-8'))
    sign =md.hexdigest()
    data = {
        "appid": appid,
        "q": text,
        "from": 'auto',
        "to": 'en',
        "salt": salt,
        "sign": sign
    }
    response = requests.post('https://fanyi-api.baidu.com/api/trans/vip/translate', params= data, headers={'Content-Type': 'application/x-www-form-urlencoded'}) 
    text = response.json()
    results = text['trans_result'][0]['dst']
    return results

from googletrans import Translator
def _finalTranslate(t):
    retry = 0
    while retry < 3:
        try:
            en_t = translate.translate(t, dest='en').text
            return en_t
        except:
            time.sleep(2)
            retry+=1
            continue
    return _translateWithBaidu(t)
import langid
import re
translate = Translator()
def _translate(t):
    try:
        if langid.classify(t)[0] == 'zh':
            return _finalTranslate(t)
        else:
            return t
    except Exception as e:
        return t
def downloadPosts(country, task_id, uuid, data, group_id, gallery_name, user_type):
    global groupCacheConfig
    global allCount
    global currentCount
    global user_id
        
    post_text = data["text"]
    other_gallery_name = ""
    try:
        if "#" in post_text:
            tags = re.findall(r'#\w+', post_text)
            for t in tags:
                other_gallery_name += f",{_translate(t[1:])}"
            post_text = re.sub(r'#\w+', '', post_text).strip()
        post_text = _translate(post_text)
    except Exception as e:
        print("translate fail!")
    medias = data["medias"]
    BR_USER = ["Cyberpynk","Paintings","Pop Art","Architecture","Interior Design","Space"]
    groupCacheConfig[task_id][uuid] = {
        "gallery_name": f"{gallery_name}{other_gallery_name}", #utils.randomGellaryText()
        "user_type": user_type if len(user_type)>0 else BR_USER[random.randint(0, len(BR_USER)-1)],
        "group_id":0,
        "user_id":user_id,
        "post":[]
    }
    idx = 0
    allCount += len(medias)
    for it in medias:
        media_type = it["media_type"]
        media_resource_url = it["resource_url"]
        medoa_cover_url = it["preview_url"]
        audio_resource_url = ""
        if "formats" in it:
            formats = it["formats"]
            quelity = 0
            for format in formats:
                if format["quality"] > quelity and format["quality"] <= 1080:
                    quelity = format["quality"]
                    media_resource_url = format["video_url"]
                    audio_resource_url = format["audio_url"]
        try:
            mecordType = mediatype2mecord(media_type)
            ossurl, cover_url = download(country, media_type, post_text, media_resource_url, audio_resource_url, medoa_cover_url, task_id)
            logging.info(f"{country} === upload: {ossurl} cover={cover_url}")
            currentCount+=1
            print(f"{country} === {task_id} : {currentCount}/{allCount}")
            global firstMediaCover
            if len(firstMediaCover) <= 0:
                firstMediaCover = cover_url
            title = post_text
            if len(title) > 100:
                title = title[0:100]
            groupCacheConfig[task_id][uuid]["post"].append({
                "widget_id": 169,
                "content": [ ossurl ],
                "info": [post_text], #"<tid:0>"表示视频直接发
                "content_type": mecordType,
                "cover_url": cover_url,
                "title": title,
                "generate_params": "",
            })
            utils.idlingService(isWorking=True)
            time.sleep(0.5)
            if currentCount > 10:
                processPosts(country, task_id, group_id, gallery_name, user_type)
                currentCount = 0
        except Exception as e:
            print(f"{country} ====================== download+process+upload error! ======================")
            print(e)
            print(f"{country} ======================                                ======================")
            time.sleep(10)  # maybe Max retries
        idx += 1

def aaaapp(country, task_id, group_id, url, gallery_name, user_type, cursor = "", page = 0):
    if len(url) <= 0:
        return

    global user_id
    param = {
        "userId": "D042DA67F104FCB9D61B23DD14B27410",
        "secretKey": "b6c8524557c67f47b5982304d4e0bb85",
        "url": url,
        "cursor": cursor,
    }
    requestUrl = "https://h.aaaapp.cn/posts"
    logging.info(f"{country} === request: {requestUrl} param={param}")
    s = requests.session()
    s.keep_alive = False
    res = s.post(requestUrl, params=param, verify=False)
    if len(res.content) > 0:
        data = json.loads(res.content)
        if data["code"] == 200:
            posts = data["data"]["posts"]
            for it in posts:
                post_id = it["id"]
                downloadPosts(country, task_id, f"{group_id}_{post_id}", it, group_id, gallery_name, user_type)
                if page == 0 and user_id == 0:
                    user_id = updateUser(country, task_id, group_id, url, data["data"]["user"])
                    print(f"{country} === add user {user_id}")
                    logging.info(f"{country} === add user {user_id}")


            if "has_more" in data["data"] and data["data"]["has_more"] == True:
                next_cursor = ""
                if "next_cursor" in data["data"]:
                    next_cursor = str(data["data"]["next_cursor"])
                    if "no" in data["data"]["next_cursor"] and len(next_cursor) <= 0:
                        next_cursor = ""
                if len(next_cursor) > 0:
                    aaaapp(country, task_id, group_id, url, gallery_name, user_type, next_cursor, page + 1)
        else:
            print(f"{country} === error aaaapp, context = {res.content}")
            logging.info(f"{country} === error aaaapp, context = {res.content}")
            if data["code"] == 300:
                print(f"{country} === no money, exit now!")
                logging.info(f"{country} === no money, exit now!")
                utils.notifyServiceStop("没钱了")
                exit(-1)
            else:
                utils.idlingService(isWorking=False)
    else:
        print(f"{country} === error aaaapp, context = {res.content}, eixt now!")
        logging.info(f"{country} === error aaaapp, context = {res.content}, eixt now!")
        utils.notifyServiceStop(res.content)
        exit(-1)
    s.close()

def do_aaaapp_crawler(country):
    global allCount
    global user_id
    global currentCount
    global groupCacheConfig

    s = requests.session()
    s.keep_alive = False
    res = s.get(f"https://{domain(country)}/proxymsg/crawler/get_task?t={random.randint(100, 99999999)}",
                verify=False, timeout=60)
    s.close()
    if len(res.content) > 10:
        try:
            cf = json.loads(res.content)
        # dddd = "{\"code\":0,\"msg\":\"\",\"data\":{\"info\":{\"id\":0,\"link_url\":\"https://www.tiktok.com/@adrianwang11?is_from_webapp=1&sender_device=pc\",\"user_type\":\"Indonesia\",\"gallery_name\":\"BeautyfulGirl\",\"group_id\":100138}}}"
        # if len(dddd) > 0:
        #     cf = json.loads(dddd)
            if cf["code"] == 0:
                if "info" in cf["data"]:
                    data = cf["data"]["info"]
                    taskid = str(data["id"])
                    link_url = data["link_url"]
                    gallery_name = data["gallery_name"]
                    user_type = ""
                    if "user_type" in data:
                        user_type = data["user_type"]
                    group_id = 0
                    if "group_id" in data:
                        group_id = data["group_id"]
                    group_id = 100138
                    user_id = 0
                    logging.info(f"{country} ================ begin group-crawler {taskid} : {group_id} ===================")
                    print(f"{country} ================ begin group-crawler {taskid} : {group_id} ===================")
                    allCount = 0
                    currentCount = 0
                    groupCacheConfig = {}
                    groupCacheConfig[taskid] = {}
                    start_pts = calendar.timegm(time.gmtime())
                    utils.idlingService(isWorking=True)
                    aaaapp(country, taskid, group_id, link_url, gallery_name, user_type)
                    processPosts(country, taskid, group_id, gallery_name, user_type)
                    current_pts = calendar.timegm(time.gmtime())
                    logging.info(f"{country} ================ finish group-crawler {taskid} : {group_id} : {user_id} duration:{current_pts - start_pts} ==============")
                    print(f"{country} ================ finish group-crawler {taskid} : {group_id} : {user_id} duration:{current_pts - start_pts} ==============")
                    return
        except Exception as e:
            logging.error(f"{country} ====================== uncatch Exception ======================")
            logging.error(e)
            logging.error(f"{country} ======================      end      ======================")
            print(f"{country} ====================== uncatch Exception ======================")
            print(e)
            print(f"{country} ======================      end      ======================")