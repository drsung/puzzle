import random
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import functools
import dialog
import problem
import images
class Tile(QLabel):
    def __init__(self,text,parent = None):
        super(Tile,self).__init__(parent)
        self.resize(100,100)
        self.text = text
    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setBrush(QColor(5,57,74,100))
        painter.setPen(Qt.black)

        if self.text == '0':
            painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(QPaintEvent.rect())
        painter.setPen(QColor(255,255,255,200))
        font = QFont()
        font.setPointSize(14)
        painter.setFont(font)
        painter.drawText(QPaintEvent.rect(),Qt.AlignCenter,str(self.text))

    def setTile(self,text):
        self.text = text
        self.update()
class Window(QWidget):
    def __init__(self,parent = None):
        super(Window,self).__init__(parent)
        self.startState = [1,2,3,8,0,4,7,6,5]
        self.initTile()
        self.initBoard()
        self.drawBoard()
        self.setMaximumSize(500,600)
        self.setMinimumSize(500,600)
        button = QPushButton("Solve",self)
        button.move(200,500)
        button.clicked.connect(self.btnclick)
        self.goalState = [[1,2,3],[8,0,4],[7,6,5]]
        self.button2 = QPushButton("Create",self)
        self.button2.move(200,450)
        self.bg = QPixmap(":/bg.png")
        self.button2.clicked.connect(self.create)
        self.setWindowTitle("8-Puzzle")
        self.setWindowIcon(QIcon(':/icon.png'))
    def create(self):
        self.showDialog()
        self.initBoard()
        self.drawBoard()
    def showDialog(self):
        d = dialog.dialog()
        if d.exec_():
            self.startState = d.getState()
    def drawBoard(self):
        for x in range(3):
            for y in range(3):
                if (self.board[x][y]):
                    self.board[x][y].move(100+100*y+3*y,100+100*x+3*x)
    def initTile(self):
        self.tile=[]
        for x in range(8):
            self.tile.append(Tile("0",self))

    def initBoard(self):
        value = self.startState
        #random.shuffle(value)
        tileIndex = 0
        index = 0
        self.board = []
        for x in range(3):
            column = []
            for y in range(3):
                if value[index]!=0:
                    self.tile[tileIndex].setTile(value[index])
                    column.append(self.tile[tileIndex])
                    tileIndex+=1
                else:
                    column.append(None)
                index+=1
            self.board.append(column)
    def direction(self,des,cur):
        return QPoint(cur[1]-des[1],cur[0]-des[0])
    def convertToPixel(self,x,y):
        return 100+y*100+y*3, 100+x*100+x*3
    def getStartState(self):
        state = []
        for x in range(3):
            column = []
            for y in range(3):
                if (self.board[x][y]!=None):
                    column.append(int(self.board[x][y].text))
                else:
                    column.append(0)
            state.append(column)
        return state
    def btnclick(self):
        startState = self.getStartState()
        if startState == self.goalState:
            print('Solved!')
            return
        newProblem = problem.Problem()
        solve = problem.Solve_Problem()
        newProblem.setStartState(startState)
        newProblem.setGoalState(self.goalState)
        step, cost, nodeExpanded = solve.getAnswer(newProblem)
        msg = QMessageBox()
        if(cost == -1):
            msg.setWindowTitle("Not Found")
            text = "Not found solution!"
        else:
            msg.setWindowTitle("Solution found")
            text = "Node Expanded: "+str(nodeExpanded) +".\nCost: " + str(cost) + " step."
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        self.solve(step)


    def swapTile(self,cur,des,step):
        nextTilePos = self.board[des[0]][des[1]].pos()
        x,y = self.convertToPixel(cur[0],cur[1])
        blankPos = QPoint(x,y)
        if nextTilePos != blankPos:
            QTimer.singleShot(15,functools.partial(self.moveTile,cur,des,step))

    def moveTile(self,cur,des,step):
        velocity = self.direction(des,cur) * 7
        nextTilePos = self.board[des[0]][des[1]].pos()
        x,y = self.convertToPixel(cur[0],cur[1])
        blankPos = QPoint(x,y)
        distance = (blankPos.x()-nextTilePos.x())+(blankPos.y()-nextTilePos.y())
        distance = abs(distance)
        if (distance < 7):
            self.board[des[0]][des[1]].move(blankPos)
            temp=self.board[cur[0]][cur[1]]
            self.board[cur[0]][cur[1]] = self.board[des[0]][des[1]]
            self.board[des[0]][des[1]] = temp
            QTimer.singleShot(15,functools.partial(self.solve,step))
        else:
            self.board[des[0]][des[1]].move(nextTilePos+velocity)
            QTimer.singleShot(15,functools.partial(self.swapTile,cur,des,step))
    def solve(self,step):
        if len(step)>1:
            cur = step[0]
            des = step[1]
            del step[0]
            QTimer.singleShot(15,functools.partial(self.swapTile,cur,des,step))
    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.drawPixmap(QPoint(0,0),self.bg)




app = QApplication(sys.argv)
w = Window()
w.show()
app.exec_()
