#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@Time: 2021/11/19 11:39:22
@Author: zhangqiang 
@Contact: 504725439@qq.com 
'''

import pymel.core as pm
import maya.cmds as cmds
from vendor.Qt import QtWidgets,QtGui,QtCore
from util.mayautil import *
import os
from functools import partial
from pathutil import *

class shelfCreate(object):
    """create maya shelf tools from libs path

    Args:
        object ([type]): [description]
    """

    def __init__(self):
        self.__shelf_name = "shelf_test"
        self.__gMainShelf = pm.mel.eval("$tmp=$gShelfTopLevel;")
        self.__thisShelf = None
        self.__shelf_Qt = None
        self.__tools_dir = getToolsPath()
        self.__tools_dir = r"W:\xTools\tools"
        self.__tools_btns = []
        self.__optionText = None
        self.__optionList = [
            "Modeling","Rigging","Animation","FX","Rendering","All"
        ]
        
    def create_shelf(self):
        if pm.shelfLayout(self.__shelf_name,q=1,ex=1):
            pm.deleteUI(self.__shelf_name)
        self.__thisShelf = pm.shelfLayout(self.__shelf_name,p=self.__gMainShelf)
        pm.shelfLayout(self.__thisShelf,e=1,spa=5)
        self.__shelf_Qt = getMayaWidgetFromName(self.__thisShelf)
        self.createOption()

        self.__tools_btns = []
        for tool in self.getTools():
            toolbtn = self.addToolButton(tool)
            self.__tools_btns.append(toolbtn)
    def getTools(self):
        """get tools from libs path

        Returns:
            list: [{name:toolName,icon:toolicon,scriptFile:*.mel/*.py,scriptType:mel/py}] 
        """

        reslute  = []
        if not os.path.isdir(self.__tools_dir):
            return reslute
        
        for tDir in os.listdir(self.__tools_dir):
            toolpath = os.path.join(self.__tools_dir,tDir)
            tmpToolValue = {}
            tmpToolValue["scriptFiles"] = []
            if os.path.isfile(toolpath):
                filetype = tDir.split(".")[-1].lower()
                tmpToolValue["name"] = tDir.split(".")[0]
                if filetype=="mel" or filetype=="py":
                    tmpToolValue["scriptFiles"].append(rePath(toolpath))
                if tmpToolValue.get("scriptFiles"):
                    reslute.append(tmpToolValue)
            elif os.path.isdir(toolpath):
                tmpToolValue["name"] = tDir
                for f in os.listdir(toolpath):
                    file = os.path.join(toolpath,f)
                    if os.path.isfile(file):
                        filetype = f.split(".")[-1].lower()
                        if filetype=="png":
                            tmpToolValue["icon"] = rePath(file)
                        elif filetype == "mel" or filetype=="py":
                            tmpToolValue["scriptFiles"].append(rePath(file))
                            
                if tmpToolValue.get("scriptFiles"):
                    reslute.append(tmpToolValue)


        return reslute
    def createOption(self):
        
        pm.setParent(self.__thisShelf)

        pm.optionMenu(changeCommand=self.onOptionChanged,w=100)
        for i in self.__optionList:
            pm.menuItem(l=i)

        #pm.rowLayout(nc=2,adj=1,cw2=(10,12),ct2=["both"]*2,w=100,bgc=[0.21]*3)

        # self.__optionText = pm.text(l=self.__optionList[0],bgc=[0.21]*3,h=20,hlc=(0.1,0.2,0.3))
        # typeSelectBtn = pm.iconTextButton(st="iconOnly",i="Tree_Expanded_Down.png")
        # p=pm.popupMenu(b=1)
        # for i in self.__optionList:
        #     pm.menuItem(p=p,l=i,c=partial(self.changeShelfOption,i))
        pm.menuItem(d = 1)
        pm.menuItem(l="change height",c=self.changeShelfWidgetHeight)
        # pm.setParent("..")
        pm.setParent("..")
    
    def onOptionChanged(self,option):
        
        if option=="All":
            for btn in self.__tools_btns:
                btn.setVisible(1)
        elif option=="change height":
            self.changeShelfWidgetHeight()
        else:
            for btn in self.__tools_btns:
                btn.setVisible(option=="Animation")
            

    
    def getShelfQt(self):
        return self.__shelf_Qt

    def addToolButton(self,tool):
        
        iconPath = tool.get("icon")
        scriptFiles = tool.get("scriptFiles")
        w =len(tool.get("name")) *7 if len(tool.get("name")) * 7 > 32 else  32
        if len(scriptFiles)==1:
            toolbtn = pm.iconTextButton(l=tool.get("name"),st="textOnly",ann="...",w=w,p=self.__thisShelf,c=partial(execScriptFile,scriptFiles[0]))
        else:
            toolbtn = pm.iconTextButton(l=tool.get("name"),st="textOnly",ann="...",w=w,p=self.__thisShelf)
            p = pm.popupMenu(b=1)
            for script in scriptFiles:
                filename = os.path.basename(script).split(".")[0]
                pm.menuItem(p=p,l=filename,c=partial(execScriptFile,script))

            pm.setParent("..")
        if not iconPath:
            return toolbtn
        if os.path.isfile(iconPath):
            w=32
            try:
                size = QtGui.QPixmap(iconPath).size()
                w *= (size.width()/size.height()) 
            except:pass
            pm.iconTextButton(toolbtn,e=1,st="iconOnly",i=iconPath,w=w)
        return toolbtn
    def changeShelfWidgetHeight(self,*args):
        value = 100 if pm.tabLayout(self.__gMainShelf,q=1,h=1) == 64 else  64
        pm.tabLayout(self.__gMainShelf,e=1,h=value)

global gShelfCreate
gShelfCreate = None
def main():
    gShelfCreate = shelfCreate()
    gShelfCreate.create_shelf()
if __name__ == "__main__":
    main()