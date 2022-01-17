
from PySide2 import QtWidgets

class UIWidget(object):
    """class that will be inherited to do things like showUI"""

    ui_name  = "widget" #the name that will be used to find the UI in __main__

    def __init__(self,*args,**kwargs):
        pass

    def cleanupOnClose(self):
        """implement any cleaup code here"""

    @classmethod
    def showUI(cls, *args, **kwargs):
        """creates and instance then shows the UI"""

        ui = cls.createInstance(*args, **kwargs)
        ui.show()
        return ui

    @classmethod
    def createInstance(cls, *args, **kwargs):
        """create an instance of the UI - kills any existing instances"""

        import __main__
        windows = __main__.__dict__.setdefault("qt_windows", {})

        #get the ui name and if it's open, close it before re-instantiating
        ui = windows.get(cls.ui_name)
        if ui:
            ui.close()
        windows[cls.ui_name] = cls(*args, **kwargs)

        return windows[cls.ui_name]



class UIWindow( QtWidgets.QWidget,UIWidget ):

    #UI name that to find the UI instance - used in showUI()
    ui_name = "window"

    def __init__(self,*args,**kwargs):
        super(UIWindow, self).__init__(*args,**kwargs)


    def setupUi(self, window):
        super(UIWindow, self).setupUi(window)


    def show(self):
        super(UIWindow, self).show()

    def showEvent(self, event):
        """show event"""
        super(UIWindow, self).showEvent(event)

    def closeEvent(self, event):
        """called when the UI is closed"""

        #gets called on cleanup
        self.cleanupOnClose()        

    def cleanupOnClose(self):
        """implement any cleaup code here"""
        print("cleaning up on close")




class exsample_window(UIWindow,QtWidgets.QScrollArea):

    ui_name = "exsample_window"

    def __init__(self,*args):
       super(exsample_window,self).__init__(*args)

       

    

if __name__ =="__main__":

    

    exsample_window.showUI()