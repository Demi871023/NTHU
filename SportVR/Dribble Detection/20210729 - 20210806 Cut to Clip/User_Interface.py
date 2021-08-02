import sys

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStyle, 
    QSizePolicy, 
    QFileDialog
)
from PyQt5.QtGui import QPalette, QColor, QIcon

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib



class Color(QWidget):
    
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dribbling Clip")
        self.setGeometry(0, 0,  1280, 720)

        Main_Layout = QHBoxLayout()
        # Main_Layout.addWidget(Color('red'))
        Video_Result_Layout = QVBoxLayout()
        Main_Layout.addLayout(Video_Result_Layout)
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videowidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(videowidget)
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_video)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        VideoControl_Layout = QHBoxLayout()
        VideoControl_Layout.setContentsMargins(0, 0, 0, 0)
        VideoControl_Layout.addWidget(openBtn)
        VideoControl_Layout.addWidget(self.playBtn)
        VideoControl_Layout.addWidget(self.slider)

        Video_Layout = QVBoxLayout()
        Video_Layout.addWidget(videowidget)
        Video_Layout.addLayout(VideoControl_Layout)
        Video_Layout.addWidget(self.label)

        Video_Result_Layout.addLayout(Video_Layout)
        
        

        
        # 繪圖
        self.input = QLineEdit()
        self.input.textChanged.connect(self.update_chart)
        self.canvas = FigureCanvas(plt.Figure(figsize = (15, 6)))




        Video_Result_Layout.addWidget(self.input)
        Video_Result_Layout.addWidget(self.canvas)

        self.insert_ax()


        widget = QWidget()
        widget.setLayout(Main_Layout)
        # self.mediaPlayer.setVideoOutput(videowidget)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


    def open_video(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MeidaPause)
            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )


    def insert_ax(self):
        self.ax = self.canvas.figure.subplots()
        self.ax.set_ylim = ([0, 100])
        self.ax.set_xlim = ([0, 1])
        self.bar = None


    def update_chart(self):
        value = self.input.text()
        try:
            val = float(value)
        except ValueError:
            Value = 0

        x_position = [0.5]

        if self.bar:
            self.bar.remove()
        self.bar = self.ax.bar(x_position, value, width = 0.3, color = 'g')
        self.canvas.draw()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()