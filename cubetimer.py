import sys, keyboard, os, json, random

from cubescrambler import scrambler333

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from PyQt5.QtCore import QTime, QTimer, Qt, pyqtSignal




class Stopwatch(QWidget):
    file_path = "YOUR SOLVE TIMES FILE"
    scramble_file = "YOUR JSON FILE"
    trigger = pyqtSignal()
    reset_trigger = pyqtSignal()
    
    
    
    
    
    def __init__(self):
        
        super().__init__()

        self.backGround = QLabel(self)
        
        self.time = QTime(0,0,0,0)
        
        self.colors = ["Red", "Yellow", "Green", "Pink", "White", "Blue"]
        
        self.time_label = QLabel("00:00.00",self)


        self.timer = QTimer(self)

        with open(self.scramble_file, "r") as self.f:
            self.cubeScramble = json.load(self.f)
        
        self.num = 1

        self.scramble = self.cubeScramble[f"sc{self.num}"]

        
        self.cube_scramble = QLabel(f"{self.scramble}" ,self)

        self.trigger.connect(self.start_and_stop)
        self.reset_trigger.connect(self.reset)
        keyboard.add_hotkey('space', lambda: self.trigger.emit())
        keyboard.add_hotkey('e', lambda: self.reset_trigger.emit()) 
        
        self.InitUI()



    def InitUI(self):
        self.setGeometry(300,180,840,464)
        self.setWindowTitle("Cube timer")




        self.backGround.setGeometry(0,0,1336,768)
        self.backGround.setStyleSheet("background-color: hsl(0,0%,0%)")

        self.time_label.setGeometry(0,0,840,320)
        self.time_label.setStyleSheet(f"font-size: 120px; background-color: hsl(0, 0%, 0%); color: White;" \
        " padding: 0px; font-weight: bold; ")
        
        self.time_label.setAlignment(Qt.AlignCenter)

        self.cube_scramble.setGeometry(0,284,840,184)
        self.cube_scramble.setStyleSheet(f"font-size: 30px; background-color: hsl(0, 0%, 0%); color: White;" \
        " padding: 0px; ")

        self.cube_scramble.setAlignment(Qt.AlignCenter)


        self.timer.timeout.connect(self.update_display)

   
    def start_and_stop(self):
        if self.timer.isActive():
            self.timer.stop()

            with open(self.file_path, "a") as self.times_shit:
                self.times_shit.write("  " + self.time_label.text() + "\n")

            self.num = random.randint(1,357)
            self.scramble = self.cubeScramble[f"sc{self.num}"]
            
            self.cube_scramble.setText(self.scramble)

        else:
            self.timer.start(10)

    def reset(self):
        self.timer.stop()
        self.time = QTime(0,0,0,0)
        self.time_label.setText(self.format_time(self.time))

    def format_time(self,t):
        minutes = t.minute()
        seconds = t.second()
        milliseconds = t.msec()//10
        return f"{minutes:02}:{seconds:02}.{milliseconds:02}"


    def update_display(self):
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))



if  __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    stopwatch.move(app.desktop().screen().rect().center() - stopwatch.rect().center())

    sys.exit(app.exec_())   
