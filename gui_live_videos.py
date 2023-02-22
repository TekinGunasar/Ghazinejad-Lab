import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

import numpy as np
import time
import os
import cv2 as cv

from threading import Thread,activeCount

class VideoThread(QThread):
   change_pixmap_signal = pyqtSignal(np.ndarray)

   def __init__(self):
      super().__init__()
      self._run_flag = True

   def run(self):
      # capture from web cam
      cap = cv.VideoCapture('live_videos/HCS/HCS Graphic.mp4')
      while self._run_flag:
         ret, cv_img = cap.read()
         if ret:
            self.change_pixmap_signal.emit(cv_img)
      # shut down capture system
      cap.release()

   def stop(self):
      """Sets run flag to False and waits for thread to finish"""
      self._run_flag = False
      self.wait()



class MainWindow(QMainWindow):

   def __init__(self):
      super(MainWindow, self).__init__()
      self.setWindowTitle("Multimedia Lesson")

      self.display_width = 640
      self.display_height = 480

      main_layout = QHBoxLayout()
      video_selection = QVBoxLayout()

      groupbox_tensile_tests = QGroupBox('Tensile Test Videos')
      groupbox_tensile_tests.setStyleSheet("background-color:rgb(98,178,232); font-size:100px; border: 1px solid black;")

      vbox_tensile_tests = QVBoxLayout()
      groupbox_tensile_tests.setLayout(vbox_tensile_tests)

      vid_tensile_1_button = QPushButton('Video 1')
      vbox_tensile_tests.addWidget(vid_tensile_1_button)
      vid_tensile_1_button.setStyleSheet('QPushButton {border: 5px solid black; background:white;} '
                                         'QPushButton:hover {background:rgb(230,230,230)}')

      groupbox_coldworks = QGroupBox('Coldworks Videos')
      groupbox_coldworks.setContentsMargins(10,10,10,10)
      groupbox_coldworks.setStyleSheet("background-color:rgb(98,178,232); font-size:100px; border: 1px solid black;")

      vbox_coldworks = QVBoxLayout()
      groupbox_coldworks.setLayout(vbox_coldworks)

      vid_coldworks_1_button = QPushButton('Video 1')
      vid_coldworks_1_button.setStyleSheet('border: 5px solid black; background:white;')
      vbox_coldworks.addWidget(vid_coldworks_1_button)

      video_selection.addWidget(groupbox_tensile_tests)
      video_selection.addWidget(groupbox_coldworks)

      main_layout.addLayout(video_selection)


      video_player = QGroupBox("Video will be Displayed Here")
      video_player.setStyleSheet("font-size:50px;")

      video_player.setStyleSheet(("background-color:white;"))
      main_layout.addWidget(video_player,10)

      video_player_vbox = QVBoxLayout()

      self.image_label = QLabel(self)
      video_player_vbox.addWidget(self.image_label,10)

      video_player.setLayout(video_player_vbox)

      self.thread = VideoThread()

      self.thread.change_pixmap_signal.connect(self.update_image)

      self.thread.start()

      widget = QWidget()
      widget.setLayout(main_layout)

      self.setCentralWidget(widget)

   def closeEvent(self, event):
      self.thread.stop()
      event.accept()

   @pyqtSlot(np.ndarray)
   def update_image(self, cv_img):
      qt_img = self.convert_cv_qt(cv_img)
      self.image_label.setPixmap(qt_img)

   def convert_cv_qt(self, cv_img):
      rgb_image = cv.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
      h, w, ch = rgb_image.shape
      bytes_per_line = ch * w
      convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
      p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
      return QPixmap.fromImage(p)


def main():
   app = QApplication(sys.argv)
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())


if __name__ == '__main__':
   main()