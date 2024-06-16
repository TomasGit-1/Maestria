import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QSlider, QSpinBox
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtCore import QThread, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
# from CameraThread import CameraThread
import cv2 as cv
import numpy as np

class MainWindow(QWidget):
    lower_blue = np.array([50, 50, 50])
    upper_blue = np.array([130, 255, 255])
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenCV and PyQt5 Example")
        self.setupUI()
        self.camera = cv.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.lower_blue = np.array([50, 50, 50])
        self.upper_blue = np.array([130, 255, 255])

    def setupUI(self):
        self.label_original = QLabel(self)
        self.label_mask = QLabel(self)
        self.label_result = QLabel(self)

        self.label_original.setFixedSize(320, 240)  
        self.label_mask.setFixedSize(320, 240)      
        self.label_result.setFixedSize(320, 240) 

        self.slider_hue_lower = self.create_slider("Hue Lower", self.lower_blue, 0)
        self.slider_hue_upper = self.create_slider("Hue Upper", self.upper_blue, 0)

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.slider_hue_lower)
        control_layout.addWidget(self.slider_hue_upper)
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.label_original)
        layout.addWidget(self.label_mask)
        layout.addWidget(self.label_result)
        layout.addWidget(self.slider_hue_lower)
        layout.addLayout(control_layout)

        self.setLayout(layout)
    
    def create_slider(self, label_text, color_array, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.setValue(color_array[0])
        slider.valueChanged.connect(lambda value, array=color_array, index=0: self.update_color(value, array, index))
        return slider

    def update_lower_blue(self):
        self.lower_blue = np.array([self.slider_hue_lower.value(),
                                    self.slider_saturation_lower.value(),
                                    self.slider_value_lower.value()])

    def update_color(self, value, color_array, index):
        print(f"Update {value} ")
        color_array[index] = value

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            lower_blue = np.array([50, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask = cv.inRange(hsv, lower_blue, upper_blue)
            res = cv.bitwise_and(frame, frame, mask=mask)

            self.display_frame(frame, self.label_original)
            self.display_frame(mask, self.label_mask)
            self.display_frame(res, self.label_result)

    def display_frame(self, frame, label):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qImg))
        label.setAlignment(Qt.AlignCenter)

    def closeEvent(self, event):
        self.camera.release()
        event.accept()