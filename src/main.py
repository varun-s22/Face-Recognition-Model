from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel
import sys
from face_recognize import recognize
from face_train import trainModel,takePicture
from collections import namedtuple,defaultdict
from csv import reader
from PyQt6.QtGui import QPainter, QBrush,QColor
from PyQt6.QtCore import Qt
import os

userData=namedtuple("userData","name,id")
data=defaultdict(lambda Str:Str)

class LoginScreen(QWidget):
    ''' Creates a seperate window, for the logged in users
        Shows a message on dashboard, if recognized
        
        else, shows an error message
    '''
    def __init__(self,userName:str) -> None:
        # takes name of the user logged in, as parameter

        super().__init__()
        # inherits from QWidget
        self.setWindowTitle("Security System")
        self.setStyleSheet("background-color:#f5f5ef;font-family:Verdana;font-size:30px;color:#363739")
        self.setFixedHeight(600)
        self.setFixedWidth(1000)

        # text
        self.label=QLabel(self)
        self.label.move(250,330)

        if(userName is not None):
            # if registered
            self.label.setText(f"Welcome to the Dashboard, {userName}")
        else:
            self.label.setText("Sorry!! You are not registered")

class MyWindow(QWidget):
    '''
        Creates a window, for the facial recognition security system
        Iniitally it creates a blank window, then on calling its member functions
        it creates a GUI window with features.
    '''
    def __init__(self) -> None:
        super().__init__()
        # inherits from QWidget
        self.setWindowTitle("Security System")
        self.setStyleSheet("background-color:#f5f5ef;font-family:Verdana;font-size:20px;color:#363739")
        self.setFixedHeight(600)
        self.setFixedWidth(1000)

        # input fields
        self.userName=self.createInput("Name",620,180,630,220)
        self.id=self.createInput("ID",620,280,630,320)

        # text to display
        message="Already have an account? Click here to"
        h1="Security"
        h2="System"
        h3="..."
        self.h4="Sign up!!"

        # calling member functions to build main page
        self.createLineLeft(h3,40,60)
        self.createLineLeft(h1,50,170)
        self.createLineLeft(h2,80,320)
        self.createLineRight(message,500,470)
        self.createLineRight(self.h4,630,90)
        self.createButton("Register",670,400,100,50,trainModel)
        self.createButton("Login",900,465,75,35,recognize)

    def paintEvent(self,event) -> None:
        # draws a figure on the side of the window
        painter=QPainter(self)
        brush = QBrush(QColor(255,206,94),Qt.BrushStyle.SolidPattern)
        painter.setBrush(brush)
        painter.drawEllipse(-1200,-140,1700,880)
    
    def createLineLeft(self,text:str,posX:int,posY:int):
        # creates a text area on the left region, takes message and the position of text area as parameters
        label=QLabel(self)
        label.setText(text)
        label.move(posX,posY)
        label.setStyleSheet("font-size:100px;color:#363739;background-color:#ffce5e")

    def createLineRight(self,text:str,posX:int,posY:int):
        # creates a text area on the right region, takes message and the position of text area as parameters
        label=QLabel(self)
        label.setText(text)
        label.move(posX,posY)
        if(text==self.h4):
            label.setStyleSheet("font-size:45px;color:#363739")

    def createButton(self,text:str,posX:int,posY:int,width:int,height:int,func):
        # creates a button, taking the text to display, position of button, and its 2-d dimension as parameters
        self.btn=QPushButton(text,self)
        self.btn.setGeometry(posX,posY,width,height)
        self.btn.setStyleSheet("background-color:#fec062;color:#383837")
        if(text=="Register"):
            self.btn.clicked.connect(self.addData)
        else:
            if(os.path.exists("../users.csv") and os.path.isfile("../users.csv")):
                os.remove("../users.csv")
            self.btn.clicked.connect(func)
            self.btn.clicked.connect(self.showDashboard)

    def createInput(self,field:str,labelX:int,labelY:int,lineX:int,lineY:int)->QLineEdit:
        # creates input fields
        self.nameLabel=QLabel(self)
        self.nameLabel.setText(f"{field}: ")
        self.nameLabel.move(labelX,labelY)
        self.line1=QLineEdit(self)
        self.line1.resize(200,32)
        self.line1.move(lineX,lineY)
        self.line1.setStyleSheet("color:white;background-color:#363739")
        return self.line1

    def fetchData(self,line:QLineEdit)->str:
        # fetches the data after submission
        return line.text()

    def addData(self):
        # stores the data for leaning
        userTup=userData(self.fetchData(self.userName),self.fetchData(self.id))
        data[userTup.name]=userTup.id
        takePicture(userTup.name)
        trainModel(userTup.name)

    def showDashboard(self):
        # displays the dashboard after logging
        recognizedUser=None
        if(os.path.exists("../users.csv") and os.path.isfile("../users.csv")):
            with open("../users.csv","r") as csvFile:
                read=reader(csvFile)
                for row in read:
                    recognizedUser=row[0]
                    break

        # creates a new window and passes the name of identified person as argument
        self.newScreen=LoginScreen(recognizedUser)
        self.newScreen.show()
    

app=QApplication([])
# creates a window
window=MyWindow()
window.show()
sys.exit(app.exec())