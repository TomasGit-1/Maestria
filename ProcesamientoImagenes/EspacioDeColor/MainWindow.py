import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QSpinBox,QPushButton,QColorDialog
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtCore import QThread, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2 as cv
import numpy as np

class MainWindow(QWidget):
    lower_blue = np.array([50, 50, 50])
    upper_blue = np.array([130, 255, 255])

    def __init__(self):
        super().__init__()

        self.video_label = QLabel()
        self.mask_label = QLabel()
        self.res_label = QLabel()
        self.initUI()
        self.cap = cv.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10) 
        self.video_label.mousePressEvent = self.mouse_click_event
        self.lower_blue = np.array([0, 0, 0])
        self.upper_blue = np.array([179, 255, 255])

    def initUI(self):
        layout = QHBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.mask_label)
        layout.addWidget(self.res_label)
        self.setLayout(layout)
        self.setWindowTitle('Color Detection')

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, self.lower_blue, self.upper_blue)
            res = cv.bitwise_and(frame, frame, mask=mask)
            self.update_label(self.video_label, frame)
            self.update_label(self.mask_label, mask)
            self.update_label(self.res_label, res)

    def update_label(self, label, image):
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        h, w, ch = image.shape
        bytes_per_line = ch * w
        convert = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert.scaled(640, 480, aspectRatioMode=Qt.KeepAspectRatio)
        label.setPixmap(QPixmap.fromImage(p))

    def mouse_click_event(self, event):
        x = event.pos().x()
        y = event.pos().y()
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            color_rgb = frame_rgb[y, x]
            color_rgb_reshaped = np.uint8([[color_rgb]]) 
            color_hsv = cv2.cvtColor(color_rgb_reshaped, cv2.COLOR_RGB2HSV)[0][0]
            margin = np.array([10, 50, 50])
            self.lower_blue = np.maximum(color_hsv - margin, [0, 0, 0])
            self.upper_blue = np.minimum(color_hsv + margin, [179, 255, 255])
            self.update_frame()
            print(f"Color RGB en coordenadas ({x}, {y}): {color_rgb} : Color HSV {color_hsv}")
