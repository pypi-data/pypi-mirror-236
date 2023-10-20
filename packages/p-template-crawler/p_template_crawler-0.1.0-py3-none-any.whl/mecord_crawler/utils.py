import subprocess
import os
import sys
import time
import oss2
import http.client
import json
import logging
import calendar
from pathlib import Path
import shutil
import zipfile
import platform
import random
import requests
import hashlib
import ftplib
import zipfile
import datetime
from PIL import Image
from io import BytesIO
import socket
from requests_toolbelt import MultipartEncoder
from urllib import parse
import base64
import hashlib

from PIL import Image

def realCommand(cmd):
    if sys.platform != "win32":
        return "./" + " ".join(cmd)
    else:
        return cmd
    
def getOssResource(rootDir, url, md5, name):
    localFile = os.path.join(rootDir, name)
    localFileIsRemote = False
    if os.path.exists(localFile):
        with open(localFile, 'rb') as fp:
                file_data = fp.read()
        file_md5 = hashlib.md5(file_data).hexdigest()
        if file_md5 == md5:
            localFileIsRemote = True

    if localFileIsRemote == False: #download
        if os.path.exists(localFile):
            os.remove(localFile)
        s = requests.session()
        s.keep_alive = False
        print(f"download {url} ")
        file = s.get(url, verify=False)
        with open(localFile, "wb") as c:
            c.write(file.content)
        s.close()
        fname = name[0:name.index(".")]
        fext = name[name.index("."):]
        unzipDir = os.path.join(rootDir, fname)
        if os.path.exists(unzipDir):
            shutil.rmtree(unzipDir)
        print(f"unzip {url} -> {unzipDir}")

def updateBin(rootDir):
    getOssResource(rootDir, "https://m.mecordai.com/res/ffmpeg.zip", "a9e6b05ac70f6416d5629c07793b4fcf", "ffmpeg.zip.py")

    for root,dirs,files in os.walk(rootDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                print(f"unzip {os.path.join(root, name)}")
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
        if root != files:
            break

def videoInfo(file,BIN_IDX=0):
    w = 0
    h = 0
    bitrate = 0
    fps = 0
    duration = 0

    binary_dir, binary_file = ffmpegBinary(BIN_IDX)
    command = [binary_file, "-i", file]
    command = realCommand(command)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True, cwd=binary_dir)
        str = ""
        if result.returncode == 0:
            str = result.stdout.decode(encoding="utf8", errors="ignore")
        else:
            str = result.stderr.decode(encoding="utf8", errors="ignore")
        if str.find("yuv420p") > 0 and str.find("fps") > 0:
            s1 = str[str.find("yuv420p"):str.find("fps")+3].replace(' ', "")
            s1_split = s1.split(",")
            for s1_it in s1_split:
                s2 = s1_it
                if s2.find("[") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("(") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("x") > 0:
                    sizes = s2.split("x")
                    if len(sizes) > 1:
                        w = sizes[0]
                        h = sizes[1]
                if s2.find("kb/s") > 0:
                    bitrate = s2[0:s2.find("kb/s")]
                if s2.find("fps") > 0:
                    fps = s2[0:s2.find("fps")]
        if str.find("Duration:") > 0 and str.find(", start:") > 0:
            s2 = str[str.find("Duration:")+9:str.find(", start:")].replace(' ', "")
            s2_split = s2.split(":")
            if len(s2_split) > 2:
                hour = float(s2_split[0])
                min = float(s2_split[1])
                second  = float(s2_split[2])
                duration = hour*3600 + min*60 + second
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")
    return float(w),float(h),float(bitrate),float(fps),float(duration)

def ffmpegBinary(BIN_IDX=0):
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    updateBin(binDir)
    if BIN_IDX > 0:
        newBin = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"bin{BIN_IDX}")
        if os.path.exists(newBin) == False:
            shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin"), newBin)
        binDir = newBin
    binaryFile = ""
    if sys.platform == "win32":
        binaryFile = os.path.join(binDir, "ffmpeg", "win", "ffmpeg.exe")
    elif sys.platform == "linux":
        machine = platform.machine().lower()
        if machine == "x86_64" or machine == "amd64":
            machine = "amd64"
        else:
            machine = "arm64"
        binaryFile = os.path.join(binDir, "ffmpeg", "linux", machine, "ffmpeg")
    elif sys.platform == "darwin":
        binaryFile = os.path.join(binDir, "ffmpeg", "darwin", "ffmpeg")
    
    if len(binaryFile) > 0 and sys.platform != "win32":
        cmd = subprocess.Popen(f"chmod 755 {binaryFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while cmd.poll() is None:
            print(cmd.stdout.readline().rstrip().decode('utf-8'))

    if os.path.exists(binaryFile):
        return os.path.dirname(binaryFile), os.path.basename(binaryFile)
    else:
        return "", ""
    
def processMoov(file,BIN_IDX=0):
    tmpPath = f"{file}.mp4"
    binary_dir, binary_file = ffmpegBinary(BIN_IDX)
    command = [binary_file, "-i", file, "-movflags", "faststart", "-y", tmpPath]
    command = realCommand(command)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True, cwd=binary_dir)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
            os.remove(file)
            os.rename(tmpPath, file)
        else:
            logging.error("====================== ffmpeg error ======================")
            logging.error(result.stderr.decode(encoding="utf8", errors="ignore"))
            logging.error("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logging.error("====================== process error ======================")
        logging.error(e)
        logging.error("======================      end      ======================")

def ffmpegTest():
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    testImage = os.path.join(binDir, "ffmpeg", "test.jpg")
    ffmpegProcess(["-i", testImage])
    
def ffmpegProcess(args,BIN_IDX=0):
    binary_dir, binary_file = ffmpegBinary(BIN_IDX)
    command = [binary_file] + args
    command = realCommand(command)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True, cwd=binary_dir)
        if result.returncode == 0:
            logging.info(result.stdout.decode(encoding="utf8", errors="ignore"))
        else:
            logging.error("===============1111======= ffmpeg error ======================")
            logging.error(result.stderr.decode(encoding="utf8", errors="ignore"))
            logging.error("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logging.error("====================== process error ======================")
        logging.error(e)
        logging.error("======================      end      ======================")

def getOssImageSize(p):
    try:
        s = requests.session()
        s.keep_alive = False
        res = s.get(p)
        image = Image.open(BytesIO(res.content), "r")
        s.close()
        return image.size
    except:
        return 0, 0

def getLocalImageSize(p):
    try:
        image = Image.open(BytesIO(p), "r")
        return image.size
    except:
        return 0, 0

def upload(country, file, curGroupId):    
    file_name = Path(file).name
    uploadWithDir(country, f"c/{curGroupId}/{file_name}", file)

ALIYUN_OSS_CONFIG = {
    "us": {
        "ALIYUN_OSS_ENDPOINT":"http://oss-us-east-1.aliyuncs.com",
        # "ALIYUN_OSS_ENDPOINT":"https://oss-accelerate.aliyuncs.com",
        "ALIYUN_OSS_ACCESS_KEY_ID":"LTAI5tDXJKUpPk4fxqyDgK4J",
        "ALIYUN_OSS_ACCESS_SECRET_KEY":"IllpcPGTeuVheHFwL5QKFOoeOr6Har",
        "ALIYUN_OSS_BUCKET_NAME":"mecord-web",
        "ALIYUN_OSS_CDN":"m.mecordai.com"
    },
    "sg": {
        "ALIYUN_OSS_ENDPOINT":"https://oss-ap-southeast-1.aliyuncs.com",
        "ALIYUN_OSS_ACCESS_KEY_ID":"LTAI5tGBeqJgSJVDTdLjiCDq",
        "ALIYUN_OSS_ACCESS_SECRET_KEY":"k5UmE7up9Yjbk1bHFgpGOTXDSBwepf",
        "ALIYUN_OSS_BUCKET_NAME":"mecord-web-sg",
        "ALIYUN_OSS_CDN":"m-sg.mecordai.com"
    }
}
def uploadWithDir(country, dir, file, isImage=False):
    realFile = file
    realFileChanged = False
    if isImage:
        image = Image.open(file, "r")
        w = image.width
        h = image.height
        format = image.format
        if format.lower() != "webp":
            #compression cover
            fname = Path(file).name
            newFile = file.replace(fname[fname.index("."):], ".webp")
            image.save(newFile, "webp")
            image.close()
            realFile = newFile
            realFileChanged = True

    auth = oss2.Auth(ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_ACCESS_KEY_ID"], ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_ACCESS_SECRET_KEY"])
    bucket = oss2.Bucket(auth, ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_ENDPOINT"], ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_BUCKET_NAME"])
    with open(realFile, "rb") as f:
        byte_data = f.read()
    file_name = Path(realFile).name
    publish_name = f"mecord/{dir}/{file_name}" 
    bucket.put_object(publish_name, byte_data)
    if realFileChanged:
        os.remove(realFile)
    cdn = ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_CDN"]
    return f"https://{cdn}/{publish_name}"

def uploadCoverAndRemoveFile(country, dir, file):
    realFile = file
    image = Image.open(file, "r")
    w = image.width
    h = image.height
    format = image.format
    MAX_SIZE = 1024
    MAX_FILE_SIZE = 512
    realFileChanged = False
    len = os.stat(file).st_size / 1024
    if len > MAX_FILE_SIZE or w > MAX_SIZE or h > MAX_SIZE or format.lower() != "webp":
        #compression cover
        if w > MAX_SIZE or h > MAX_SIZE:
            if w > h:
                image = image.resize((MAX_SIZE, int(MAX_SIZE * (h/w))))
            else:
                image = image.resize((int(MAX_SIZE* (w/h)), MAX_SIZE))
            w = image.width
            h = image.height
        fname = Path(file).name
        newFile = file.replace(fname[fname.index("."):], ".webp")
        image.save(newFile, "webp")
        image.close()
        realFile = newFile
        realFileChanged = True

    auth = oss2.Auth(ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_ACCESS_KEY_ID"], ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_ACCESS_SECRET_KEY"])
    bucket = oss2.Bucket(auth, ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_ENDPOINT"], ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_BUCKET_NAME"], connect_timeout=60)
    with open(realFile, "rb") as f:
        byte_data = f.read()
    file_name = Path(realFile).name
    publish_name = f"mecord/{dir}/{file_name}" 
    bucket.put_object(publish_name, byte_data)
    if realFileChanged:
        os.remove(realFile)
    cdn = ALIYUN_OSS_CONFIG[country.lower()]["ALIYUN_OSS_CDN"]
    return f"https://{cdn}/{publish_name}?width={w}&height={h}"

def deepFtpUpload(file, curGroupId, ftp, remote_dir=''):
    append_dir = f'{remote_dir}'
    if len(remote_dir) > 0:
        remote_path = f'1TB01/data/mecord/{curGroupId}/{append_dir}/'
        try:
            ftp.cwd(remote_path)
        except ftplib.error_perm as e:
            if e.args[0].startswith('550'):
                # 如果远程目录不存在，则创建它
                ftp.mkd(remote_path)
                ftp.cwd(remote_path)

    s = []
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            ftp.storbinary(f'STOR {os.path.basename(file)}', f)
        s.append(f"http://192.168.3.220/01/mecord/{curGroupId}/{append_dir}{os.path.basename(file)}")
    elif os.path.isdir(file):
        for filename in os.listdir(file):
            local_file = os.path.join(file, filename)
            if os.path.isfile(local_file):
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)
                s.append(f"http://192.168.3.220/01/mecord/{curGroupId}/{append_dir}{filename}")
            elif os.path.isdir(local_file):
                subdir = os.path.join(remote_dir, filename)
                s.append(ftpUpload(local_file, curGroupId, ftp, subdir))
    return s

def ftpUpload(file, curGroupId, ftp = None):
    if not ftp:
        ftp = ftplib.FTP('192.168.3.220')
        ftp.login('xinyu100', 'xinyu100.com')

    remote_path = f'1TB01/data/mecord/{curGroupId}/'
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            # 如果远程目录不存在，则创建它
            ftp.mkd(remote_path)
            ftp.cwd(remote_path)

    s = deepFtpUpload(file, curGroupId, ftp, "")
    ftp.quit()
    return s

def randomGellaryText():
    txt = []
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    for root,dirs,files in os.walk(binDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".txt.py" and "gellary" == name:
                with open(os.path.join(root, file), "r", encoding="UTF-8") as f:
                    txt = f.readlines()
        if root != files:
            break
    txt_len = len(txt)
    rd_idx = random.randint(0, txt_len-1)
    return txt[rd_idx]

WECHAT_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=09d97da2-09f2-426e-8ab2-7833000776af"
def uploadFile2Wechat(filepath):
    params = parse.parse_qs( parse.urlparse( WECHAT_URL ).query )
    webHookKey=params['key'][0]
    upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webHookKey}&type=file'
    headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"}
    filename = os.path.basename(filepath)
    try:
        multipart = MultipartEncoder(
            fields={'filename': filename, 'filelength': '', 'name': 'media', 'media': (filename, open(filepath, 'rb'), 'application/octet-stream')},
            boundary='-------------------------acebdf13572468')
        headers['Content-Type'] = multipart.content_type
        resp = requests.post(upload_url, headers=headers, data=multipart)
        json_res = resp.json()
        if json_res.get('media_id'):
            return json_res.get('media_id')
    except Exception as e:
        return ""

def notifyServiceStart():
    notifyWechatRobot({
        "msgtype": "text",
        "markdown": {
            "content": f"爬虫<{socket.gethostname()}> 上线"
        }
    })

def notifyServiceStop(reason):
    reason_str = ""
    if len(reason) > 0:
        reason_str = f", 原因：{reason}"
    notifyWechatRobot({
        "msgtype": "text",
        "markdown": {
            "content": f"爬虫<{socket.gethostname()}> 下线{reason_str}"
        }
    })

def notifyPublishError(taskid, error_msg, info):
    notifyWechatRobot({
        "msgtype": "text",
        "markdown": {
            "content": f"爬虫<{socket.gethostname()}> 上报<{taskid}>失败, 正文:<{error_msg}>"
        }
    })
    info_file = f"{os.path.dirname(os.path.abspath(__file__))}/publish_{taskid}.txt"
    with open(info_file, 'w') as f111:
        json.dump(info, f111)
    notifyWechatRobot({
        "msgtype": "file",
        "file": {
            "media_id": uploadFile2Wechat(info_file)
        }
    })

last_working_pts = calendar.timegm(time.gmtime())
def idlingService(isWorking=False):
    global last_working_pts
    if isWorking:
        last_working_pts = calendar.timegm(time.gmtime())
        return
    
    diff = calendar.timegm(time.gmtime())-last_working_pts
    if diff >= (60.0*60.0) and diff/(60*60)%1 < 60/3600:
        machine_name = socket.gethostname()
        hour = int(float(diff)/(60.0*60.0))
        if hour>12:
            return
        if hour not in [1, 3, 7, 12]:
            return
        notifyWechatRobot({
            "msgtype": "text",
            "text": {
                "content": f"爬虫<{machine_name}> 空转{hour}小时"
            }
        })

def notifyWechatRobot(param):
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        headers = dict()
        headers['Content-Type'] = "application/json"
        res = s.post(WECHAT_URL, json.dumps(param), headers=headers, verify=False)
        s.close()
    except Exception as e:
        print(f"===== qyapi.weixin.qq.com fail ", True)