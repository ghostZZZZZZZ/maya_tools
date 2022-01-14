#!/usr/bin/env python
# -*-coding:utf-8 -*-
###########################################
# Time  : 2022.01.14
# Author: zhangqiang 
# Email : 504725439@qq.com 
###########################################

import pymel.core as pm
from functools import partial

from maya_utils import getMayaWidgetFromName


def onSliderValueChanged(widget,textValue,*args):
    value = float(textValue)
    widget.setVisible(value!=0)

def main(bs):

    windowName = "BSCHECK"

    bs = pm.PyNode(bs)
    if pm.window(windowName,q=1,ex=1):
        pm.deleteUI(windowName)
    window = pm.window(windowName,title='blendTarget Check Example')
    pm.columnLayout()
    for target in bs.w.elements():
        if "[" in target or "]" in target:
            continue
        value = pm.getAttr("%s.%s"%(bs.name(),target))
        value = round(value,4)
        pm.floatSliderGrp( target,label=target, field=True ,minValue=0.0,maxValue=1.0,pre=4,vis=value!=0)
        widget = getMayaWidgetFromName(target)
        widget.children()[2].textChanged.connect(partial(onSliderValueChanged,widget))
        pm.connectControl(target,"%s.%s"%(bs.name(),target))

    pm.showWindow( window )

if __name__ =="__main__":

    bs = pm.selected()[0].listHistory(type="blendShape")[0]
    main(bs)