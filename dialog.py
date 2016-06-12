import sys
import images
from PyQt4.QtGui import *
from PyQt4.QtCore  import *
class dialog(QDialog):
    def __init__(self,parent = None):
        super(dialog,self).__init__(parent)
        self.setMinimumSize(400,500)
        self.setMaximumSize(400,500)
        self.isFocus = False
        self.textFocus = None
        self.focusRect = None
        self.state = [None]*9
        self.curStatePos = None
        btn = QPushButton("Create",self)
        btn.move(150,380)
        btn.clicked.connect(self.accept)
        self.setWindowTitle("Create Board")
        self.setWindowIcon(QIcon(':/icon.png'))
        self.bg = QPixmap(":/bg2.png")
    def resetBoard(self):
        for i in range(9):
            self.state[i]=None
        self.textFocus = None
    def checkBoard(self):
        zeroCount = 0

        for i,cell in enumerate(self.state):
            if cell==None:
                self.state[i]=0
                zeroCount+=1
            elif cell==0:
                zeroCount+=1
        if zeroCount>1:
            return False
        else:
            return True
    def accept(self):
         if self.checkBoard()==False:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Puzzle khong hop le")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self.resetBoard()
            self.update()
         else:
            QDialog.accept(self)
    def getState(self):
        return self.state
    def paintEvent(self,event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(0,0),self.bg)
        font = QFont()
        font.setPointSize(12)
        painter.setFont(font)
        painter.setPen(Qt.NoPen)
        #draw board
        painter.setBrush(QColor(255,0,0,127))
        painter.setPen(Qt.NoPen)
        for x in range(3):
            for y in range(3):
                painter.drawRect(80+x*80+2*x,100+y*80+2*y,80,80)
        if self.isFocus:
            painter.setBrush(QColor(252,117,23))
            painter.setPen(QColor(255,255,255,127))
            painter.drawRect(self.focusRect)
        if self.textFocus:
            painter.setPen(Qt.white)
            painter.drawText(self.focusRect,Qt.AlignCenter,str(self.textFocus))
        painter.setPen(Qt.white)
        for i in range(9):
            if self.state[i]!=None:
                x,y = self.indexToPos(i)
                painter.drawText(QRect(80+82*y,100+82*x,80,80),Qt.AlignCenter,str(self.state[i]))
    def mousePressEvent(self,event):
        if self.inBoard(event):
            if self.focusRect:
                if self.focusRect == self.getRect(event):
                    return
            self.isFocus = True
            self.focusRect = self.getRect(event)
            self.textFocus = None
            self.curStatePos = self.getStatePos(event)
            self.update()
        else:
            self.curStatePos = None
            self.isFocus = False
            self.textFocus = None
            self.focusRect = None
            self.update()

    def getRect(self,event):
        x= event.pos().x()
        y= event.pos().y()
        xPos = int((x-80)/82)
        yPos = int((y-100)/82)
        xPixel = 80+82*xPos
        yPixel = 100 + 82*yPos
        return QRect(xPixel-10,yPixel-10,100,100)
    def getStatePos(self,event):
        x= event.pos().x()
        y= event.pos().y()
        yPos = int((x-80)/82)
        xPos = int((y-100)/82)
        return xPos*3 + yPos
    def inBoard(self,event):
        x= event.pos().x()
        y= event.pos().y()
        if x>=80 and x<=80+82*2+80:
            if y>=100 and y<=100 + 82*2 +80:
                return True
        else:
            return False
    def keyPressEvent(self, Event):
        if self.isFocus:
            if Qt.Key_0 <= Event.key() <= Qt.Key_8:
                self.textFocus = Event.key()-48
                if (self.textFocus in self.state):
                    self.state[self.state.index(self.textFocus)] = None
                self.state[self.curStatePos] = self.textFocus

                self.update()
    def indexToPos(self,index):
        x = int(index/3)
        y = index - x*3
        return(x,y)