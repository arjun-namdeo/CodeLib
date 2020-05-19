import sys,csv,os,fnmatch,re
from PyQt4 import QtCore, QtGui, uic

from QDarkStyle import qdarkstyle

MainDirectory  = os.path.dirname(__file__).replace("\\", "/")

UIFilePath = MainDirectory + 'qtMsg.ui'
sys.path.append(MainDirectory)

class MessageWindow(QtGui.QMainWindow):
    '''
    Comments
    '''

    def __init__(self):
        '''
        constructor
        '''

        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi(UIFilePath)
        
        self.ui.show()
        
        
  


def showMessageWindow(winTitle="Message", icoName="Info"):
    icoPath = "E:/AD_Lab_World/Python/PyQt/Bank/icons"
    winMsgApp = QtGui.QApplication(sys.argv)
    winMsgApp.setStyleSheet(qdarkstyle.load_stylesheet())
    msgWindow = MessageWindow()
    
    
    msgWindow.ui.iconLabel.setPixmap(QtGui.QPixmap(("/".join([icoPath, str(icoName) + ".ico"]))))
    msgWindow.ui.setWindowTitle(str(winTitle))
        
    sys.exit(winMsgApp.exec_())


