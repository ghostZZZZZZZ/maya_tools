#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@Time: 2021/11/19 11:39:59
@Author: zhangqiang 
@Contact: 504725439@qq.com 
'''
import pymel.core as pm
from zq_tools import shelf_tool_create
import maya.api.OpenMaya as om
from zq_tools.path_utils import *
import sys
def build_tools():
    om.MGlobal.displayInfo("create shelf begin...")
    shelf_tool_create.main()
    om.MGlobal.displayInfo("create shelf done...")
    sys.path.append(getLibsPath())
    

if not pm.about(batch=True):
    pm.general.evalDeferred('build_tools()')
