#!/usr/bin/python3  
# -*- coding: UTF-8 -*-  
import logging  
import time  
from logging.handlers import TimedRotatingFileHandler  
import os
def logger_request_create(name):  
    # 创建logger实例对象  
    logger = logging.getLogger(name)  
    logger.setLevel(logging.DEBUG)  
    logger.propagate = False  # 阻止日志消息传递给父logger  
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    # 文件日志配置  
    fh = TimedRotatingFileHandler(  
        filename=f"./log/{name}.log", when='midnight', backupCount=30, encoding="utf-8")  
    fh.setFormatter(logging.Formatter(  
        '%(asctime)s  %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))  
    fh.setLevel(logging.INFO)  
    logger.addHandler(fh)  
  
    # 控制台日志配置  
    console_handler = logging.StreamHandler()  
    console_handler.setLevel(logging.DEBUG)  
    console_handler.setFormatter(logging.Formatter(  
        '%(asctime)s  %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))  
    logger.addHandler(console_handler)  
  
    return logger  
  
# 创建并配置logger  
logger = logger_request_create("logger")
erplogger = logger_request_create("erpdata")
# mqttserver = logger_request_create("mqttserver")
# tcpserver = logger_request_create("tcpserver")