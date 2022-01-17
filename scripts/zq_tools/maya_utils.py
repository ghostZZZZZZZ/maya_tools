#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@Time: 2021/11/19 11:39:49
@Author: zhangqiang 
@Contact: 504725439@qq.com 
'''
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as omui
import maya.OpenMayaAnim as oma
import maya.api.OpenMaya as newom
import maya.api.OpenMayaAnim as newoma
import maya.OpenMaya as om
from vendor.Qt import QtWidgets,QtGui,QtCore
from vendor.Qt import QtCompat as shiboken2
import os,sys


def getMayaMainWindow():
    """get maya main window 

    Returns:
        QWidget: maya main window
    """
    
    mayaMainWindowPtr = omui.MQtUtil.mainWindow() 
    return shiboken2.wrapInstance(long(mayaMainWindowPtr),QtWidgets.QWidget)

def getMayaWidgetFromName(name,qtType=QtWidgets.QWidget):
    """get maya window qt object from window

    Args:
        name (str): maya window name
        qtType (QtWidgets.*, optional): qt window obj. Defaults to QtWidgets.QWidget.

    Returns:
        qtType: qt window obj
    """

    windowPtr = omui.MQtUtil.findLayout(name)
    return shiboken2.wrapInstance(long(windowPtr),qtType)

def getScriptFileType(file):
    """get script file type

    Args:
        file (str): script file

    Returns:
        str: script file type
    """
    
    dotType = os.path.splitext(file)[-1].lower()
    if dotType == ".py":
        return "python"
    elif dotType == ".mel":
        return "mel"

# def htmlText(text,color,size,bold,face="Arial"):
#     outText = '<font color="%s" size = "%s" face = "%s">%s</font>' % (color,size , face , text)
#     if bold:
#         outText = "<b>" + outText + "</b>"
#     return outText


def execScriptFile(scriptFile,*args):

    """exec maya script file  mel/maya
    """

    scriptType = getScriptFileType(scriptFile)
    if scriptType == "python":
        scriptDir = os.path.dirname(scriptFile)
        libDir = os.path.join(scriptDir,"python")
        if libDir not in sys.path:
            sys.path.append(libDir)
        execfile(scriptFile)
    elif scriptType == "mel":
        pm.mel.eval('source "%s";'%scriptFile)


def getClusterWeights(cluster):
    """ get Cluster weights

    Args:
        cluster (str): cluster name

    Returns:
        [list,list]: points   weights
    """

    selection = om.MSelectionList()
    selection.add(cluster)
    clusterObj = om.MObject()
    selection.getDependNode(0,clusterObj)
    

    fnDeformer = oma.MFnWeightGeometryFilter(clusterObj)
    fnSet = om.MFnSet(fnDeformer.deformerSet())
    members = om.MSelectionList()
    fnSet.getMembers(members,False)
    dagPath = om.MDagPath()
    components = om.MObject()
    members.getDagPath(0,dagPath,components)
    weights = om.MFloatArray()
    fnDeformer.getWeights(0,components,weights)
    fnComponents = om.MFnSingleIndexedComponent(components)
    pt = om.MIntArray()
    fnComponents.getElements(pt)

    return pt,weights


def getSoftSelectionWeights():
    """get soft selection weights

    Returns:
        list,list: points, weights
    """
    
    pt = []
    weights = []
    if not cmds.softSelect(q=1,sse=1):
        return pt,weights
    richSel = newom.MGlobal.getRichSelection()
    selList = richSel.getSelection()
    selCount = selList.length()
    if selCount != 1:
        return pt,weights
    dag,comp = selList.getComponent(0)
    fnComp = newom.MFnSingleIndexedComponent(comp)
    pt = fnComp.getElements()
    weights = [fnComp.weight(i).influence for i in range(fnComp.elementCount)]
    return list(pt),weights

def create_workspace_window_contrl(window_name,window_title,ui):
    """create maya workspaceControl from Qt Window parent

    Args:
        window_name (str): window name unique
        window_title (str): window title name
        ui (QtWidgets.*): QtWidgets windows object
    """

    if not cmds.workspaceControl(window_name, q=True, exists=True):

        cmds.workspaceControl(
            window_name,
            retain=False,
            floating=True,
            #label=window_title
            #uiScript="resume_in_workspace_control()",
        )
        wrok_widget = shiboken2.wrapInstance(int(omui.MQtUtil.findControl(window_name)), QtWidgets.QWidget)
        wrok_widget.layout().addWidget(ui)
    cmds.evalDeferred(lambda *args: cmds.workspaceControl(window_name, e=True, r=True))
    cmds.workspaceControl(window_name, e=True, label=window_title)

    
    


