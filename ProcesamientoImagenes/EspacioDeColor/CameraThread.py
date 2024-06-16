from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QThread, Qt
import numpy as np
import cv2 as cv 


class CameraThread(QThread):
    """ Thread to read and display frames from a camera """
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv.VideoCapture(0)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                lower_blue = np.array([50, 50, 50])
                upper_blue = np.array([130, 255, 255])
                mask = cv.inRange(hsv, lower_blue, upper_blue)
                res = cv.bitwise_and(frame, frame, mask=mask)
                self.change_pixmap_signal.emit(res)
        cap.release()

    def stop(self):
        """ Sets run flag to False and waits for thread to finish """
        self._run_flag = False
        self.wait()