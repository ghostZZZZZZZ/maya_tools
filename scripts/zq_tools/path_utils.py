#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@Time: 2021/11/19 11:39:42
@Author: zhangqiang 
@Contact: 504725439@qq.com 
'''
import os

def rePath(path):
    return path.replace("\\","/")

def basePath():
    return rePath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def getToolsPath():
    return rePath(os.path.join(basePath(),"tools"))

def getLibsPath():

    return rePath(os.path.join(basePath(),"libs"))