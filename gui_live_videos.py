import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import numpy as np

import cv2 as cv

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

#Class making up the threading functionality needed to split into GUI thread and video frame processing thread

#Inheriting from QThread, which directly inherits from default Python threading module
class VideoThread(QThread):
   change_pixmap_signal = pyqtSignal(np.ndarray)

   def __init__(self):
      super().__init__()
      self._run_flag = True

   #overriding the 'run' function in default threading module, whenever thread.start() is called, run will be invoked
   def run(self):
      # capture from web cam
      cap = cv.VideoCapture(0)

      while self._run_flag:

         ret, cv_img = cap.read()
         if ret:
            #emitting signal, which is connected to the update_img func. to display the next video frame
            self.change_pixmap_signal.emit(cv_img)
      # shut down capture system
      cap.release()

   def stop(self):
      """Sets run flag to False and waits for thread to finish"""
      self._run_flag = False
      self.wait()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle('Multimedia Lesson')

        self.main_layout = QHBoxLayout()

        self.display_width = 1000
        self.display_height = 1000

        #Video Selection section
        self.video_selection = QVBoxLayout()
        self.main_layout.addLayout(self.video_selection,5)

        '''Adding video selection section for the tensile tests
        Involves a groupbox, and then setting the layout for that groupbox as another VBoxLayout
        for the vertically stacked buttons for the six different materials'''

        self.tensile_test_groupbox = QGroupBox('Tensile Test Videos')
        self.tensile_test_vbox = QVBoxLayout()
        self.tensile_test_groupbox.setLayout(self.tensile_test_vbox)

        #Now adding the groupbox as the first element in the video_selection vbox an styling it
        self.video_selection.addWidget(self.tensile_test_groupbox)
        self.tensile_test_groupbox.setStyleSheet("background-color:rgb(98,178,232); font-size:50px; border: 5px solid black;")

        #Adding the videos that make up the vbox layout of the tensile tests groupbox
        self.tensile_test_v1 = QPushButton('Video 1')
        self.tensile_test_vbox.addWidget(self.tensile_test_v1)
        self.tensile_test_v1.setStyleSheet('QPushButton {border: 5px solid black; background:rgb(255,255,255);} '
                                           'QPushButton:hover {background:rgb(180,180,180)}')

        #Adding video selection section now for the coldworks videos in the same manner
        self.coldworks_groupbox = QGroupBox('Coldworks Videos')
        self.coldworks_vbox = QVBoxLayout()
        self.coldworks_groupbox.setLayout(self.coldworks_vbox)

        self.video_selection.addWidget(self.coldworks_groupbox)
        self.coldworks_groupbox.setStyleSheet("background-color:rgb(98,178,232); font-size:50px; border: 5px solid black;")

        #Ading the videos that make up the vbox layout of the coldworks groupbox
        self.coldworks_v1 = QPushButton('Video 1')
        self.coldworks_vbox.addWidget(self.coldworks_v1)
        self.coldworks_v1.setStyleSheet('QPushButton {border: 5px solid black; background:rgb(255,255,255);} '
                                           'QPushButton:hover {background:rgb(180,180,180)}')

        #Video player section
        self.video_player = QVBoxLayout()

        #Making sure all the video frames will be in just on groupbox within the video player vbox
        self.video_player_groupbox = QGroupBox('Video will be displayed here')
        self.video_player_groupbox_vbox = QVBoxLayout()
        self.video_player_groupbox.setLayout(self.video_player_groupbox_vbox)

        self.video_player_groupbox.setStyleSheet('background-color:green; font-size:25px;')

        self.video_player.addWidget(self.video_player_groupbox)

        self.image_label = QLabel(self)

        self.video_player_groupbox_vbox.addWidget(self.image_label)

        self.main_layout.addLayout(self.video_player, 10)

        # Video frames stored as member proprty of this image_label variable as a Pixmap

        # Cannot display GUI elements and perform video frame processing to display on GUI
        # on the same GUI thread. Below code is using the above VideoThread class to implement
        # multithreading functionality to expand thread pool into GUI thread and video frame processing thread.

        # Much more memory efficient and performant than traditional programming.

        # Instantiating thread
        self.thread = VideoThread()

        # Whenver a 'signal' is emitted, i.e a new frame is loaded into the video, the 'update_image' function is called
        # Logic for this implemented in 'run' function in VideoThread
        self.thread.change_pixmap_signal.connect(self.update_image)

        # invokes 'run' function in video thread for this instance
        self.thread.start()

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centralWidget)

        def closeEvent(self, event):
           self.thread.stop()
           event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
       """Updates the image_label with a new opencv image"""
       qt_img = self.convert_cv_qt(cv_img)
       self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
       """Convert from an opencv image to QPixmap"""
       rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
       h, w, ch = rgb_image.shape
       bytes_per_line = ch * w
       convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
       p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
       return QPixmap.fromImage(p)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    app.exec()

if __name__ == '__main__':
    main()