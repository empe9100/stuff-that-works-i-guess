import sys, keyboard, os

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from PyQt5.QtCore import QTime, QTimer, Qt, pyqtSignal




class Stopwatch(QWidget):
    file_path = "C:/Users/empe/Desktop/cubetrimer.txt"
    trigger = pyqtSignal()
    reset_trigger = pyqtSignal()
    def __init__(self):
        
        super().__init__()

        self.time = QTime(0,0,0,0)
        self.time_label = QLabel("00:00.00")
        self.timer = QTimer(self)
        self.trigger.connect(self.start_and_stop)
        self.reset_trigger.connect(self.reset)
        keyboard.add_hotkey('space', lambda: self.trigger.emit())
        keyboard.add_hotkey('e', lambda: self.reset_trigger.emit()) 
        self.InitUI()



    def InitUI(self):
        self.setWindowTitle("Cube timer")
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)
        self.time_label.setAlignment(Qt.AlignCenter)


        self.time_label.setStyleSheet("font-size: 120px; background-color: hsl(0, 0%, 0%); color: White;" \
        " padding: 200px; font-weight: bold; ")

        self.timer.timeout.connect(self.update_display)

   
    def start_and_stop(self):
        if self.timer.isActive():
            self.timer.stop()

            with open(self.file_path, "a") as self.times_shit:
                self.times_shit.write("  " + self.time_label.text() + "\n")

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