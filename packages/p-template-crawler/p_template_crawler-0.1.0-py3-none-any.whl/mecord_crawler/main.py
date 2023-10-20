import sys
import os
import time
import platform
import logging
import urllib3
import datetime
import shutil
from urllib.parse import *

from pkg_resources import parse_version
from mecord_crawler import utils
from mecord_crawler import aaaapp_crawler
from mecord_crawler import civitai_crawler

def main():
    global rootDir

    urllib3.disable_warnings()
    d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    thisFileDir = os.path.dirname(os.path.abspath(__file__))
    logFilePath = f"{thisFileDir}/log.log"
    if os.path.exists(logFilePath) and os.stat(logFilePath).st_size > (1024 * 1024 * 5):  # 5m bak file
        d = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        bakFile = logFilePath.replace(".log", f"_{d}.log")
        shutil.copyfile(logFilePath, bakFile)
        os.remove(logFilePath)
    if parse_version(platform.python_version()) >= parse_version("3.9.0"):
        logging.basicConfig(filename=logFilePath, 
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            encoding="utf-8",
                            level=logging.INFO) 
    else:
        logging.basicConfig(filename=logFilePath, 
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)
    utils.notifyServiceStart()
    rootDir = os.path.dirname(os.path.abspath(__file__))
    while (os.path.exists(os.path.join(rootDir, "stop.now")) == False):
        try:
            #默认爬虫
            for c in ["US","SG"]:
                aaaapp_crawler.do_aaaapp_crawler(c)
            # # C站爬虫
            # civitai_crawler.civitai()
            # #组爬虫，从外网爬整个人的数据导入到mecord里
            # group_crawler.runtask()
            utils.idlingService(isWorking=False)
        except Exception as e:
            # civitai_crawler.notifyMessage(False, str(e))
            logging.error("====================== uncatch Exception ======================")
            logging.error(e)
            logging.error("======================      end      ======================")
            print("====================== uncatch Exception ======================")
            print(e)
            print("======================      end      ======================")
        time.sleep(60)
    os.remove(os.path.join(thisFileDir, "stop.now"))
    print(f"stoped !")
    utils.notifyServiceStop()

if __name__ == '__main__':
    main()