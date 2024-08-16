import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QStackedWidget, QWidget,QStackedLayout,\
                            QApplication,QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QIcon,QImage, QGuiApplication
from PyQt5.QtCore import QTimer, Qt, QSize, QPropertyAnimation, QSequentialAnimationGroup, QRect, QSize, QUrl, \
    QEasingCurve,QSizeF, pyqtProperty
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent


#set a 2d Vector to calculate position
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def to_qsize(self):
        """
        将 Vector2D transfer QSize() instance。
        """
        return QSize(self.x, self.y)


class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._opacity = 0
        self._brightness = 0.5
        self.update_style()

    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                opacity: {self._opacity};
                background-color: rgba(255, 255, 255, {int(self._opacity * 255)});
                filter: brightness({self._brightness});
            }}
        """)

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update_style()

    @pyqtProperty(float)
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.update_style()


class FullScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.start_0_animation()
        self.start_1_animation()
        self.start_2_animation()
        self.start_3_animation()
        self.start_4_animation()
        QTimer.singleShot(200,lambda : self.menu_au.play())

    def initUI(self):
        # 设置窗口为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)

        #get screen size
        screen = QGuiApplication.primaryScreen()
        size = screen.size()

        # set full screen
        self.setGeometry(0,0,size.width(),size.height())

        # Create a QLabel to display the background image
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0,0,self.width(),self.height())
        self.background_label.setPixmap(QPixmap('assets/background/background.png'))
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # Ensure the image is backward layer

        ico_size = Vector2D(340,340)
        re_size =  Vector2D(340,340)
        shrink_size = Vector2D(280,280)

        now_screen = Vector2D(0,0)

        # init update pos
        update_pos = [
            Vector2D(0,0),
            Vector2D(0,0),
            Vector2D(0,0),
            Vector2D(0,0),
            Vector2D(0,0),
            Vector2D(0, 0)
        ]

        #get screen size
        now_screen.x = size.width()
        now_screen.y = size.height()

        # print("Monitor Width:", now_screen.x)

        #desgin screen size
        des_size = Vector2D(2560,1440)
        self.des = des_size
        self.resolution = self.size().width()/self.des.x


        #update pic_0
        position_pic_0= Vector2D(135,1044)
        update_pos[0].x = int((position_pic_0.x / des_size.x) * now_screen.x )
        update_pos[0].y = int((position_pic_0.y / des_size.y) * now_screen.y)

        #update pic_1
        position_pic_1= Vector2D(620,938)
        update_pos[1].x = int((position_pic_1.x / des_size.x) * now_screen.x )
        update_pos[1].y = int((position_pic_1.y / des_size.y) * now_screen.y)

        #update pic_2
        position_pic_2= Vector2D(1050,1044)
        update_pos[2].x = int((position_pic_2.x / des_size.x) * now_screen.x )
        update_pos[2].y = int((position_pic_2.y / des_size.y) * now_screen.y)

        #update pic_3
        position_pic_3= Vector2D(1616,938)
        update_pos[3].x = int((position_pic_3.x / des_size.x) * now_screen.x )
        update_pos[3].y = int((position_pic_3.y / des_size.y) * now_screen.y)

        #update pic_4
        position_pic_4= Vector2D(2117,1010)
        update_pos[4].x = int((position_pic_4.x / des_size.x) * now_screen.x )
        update_pos[4].y = int((position_pic_4.y / des_size.y) * now_screen.y)

        # update return_to_menu
        position_rec = Vector2D(2026, 1119)
        update_pos[5].x = int((position_rec.x / des_size.x) * now_screen.x)
        update_pos[5].y = int((position_rec.y / des_size.y) * now_screen.y)

        # icon size update
        self.ico_size_update = Vector2D(0,0)
        self.ico_size_update.x = int(self.resolution * 340)
        self.ico_size_update.y = int(self.resolution * 340)

        # re_size_update
        self.re_size_update = Vector2D(0,0)
        self.re_size_update.x = int(self.resolution * 220)
        self.re_size_update.y = int(self.resolution * 220)

        btn_style = """
            background-color: transparent
        """

        menu_style = """
            background-color: transparent
        """

        # create button queue
        self.pic_0 = QPushButton('', self)
        self.pic_0.setGeometry(update_pos[0].x, update_pos[0].y,self.ico_size_update.x, self.ico_size_update.y)
        self.pic_0.setIcon(QIcon("assets/btnSet/btn_0.png"))
        self.pic_0.setIconSize(QSize(int(self.resolution * 340), int(self.resolution * 340)))
        self.pic_0.setStyleSheet(btn_style)

        self.pic_1 = QPushButton('', self)
        self.pic_1.setGeometry(update_pos[1].x, update_pos[1].y,self.ico_size_update.x, self.ico_size_update.y)
        self.pic_1.setIcon(QIcon("assets/btnSet/btn_1.png"))
        self.pic_1.setIconSize(QSize(int(self.resolution * 340), int(self.resolution * 340)))
        self.pic_1.setStyleSheet(btn_style)

        self.pic_2 = QPushButton('', self)
        self.pic_2.setGeometry(update_pos[2].x, update_pos[2].y,int(self.resolution * 340), int(self.resolution * 340))
        self.pic_2.setIcon(QIcon("assets/btnSet/btn_2.png"))
        self.pic_2.setIconSize(QSize(int(self.resolution * 340), int(self.resolution * 340)))
        self.pic_2.setStyleSheet(btn_style)

        self.pic_3 = QPushButton('', self)
        # set button position & size
        self.pic_3.setGeometry(update_pos[3].x, update_pos[3].y,self.ico_size_update.x, self.ico_size_update.y)
        self.pic_3.setIcon(QIcon("assets/btnSet/btn_3.png"))
        self.pic_3.setIconSize(QSize(int(self.resolution * 340), int(self.resolution * 340)))
        self.pic_3.setStyleSheet(btn_style)

        self.pic_4 = QPushButton('', self)
        # set button position & size
        self.pic_4.setGeometry(update_pos[4].x, update_pos[4].y,self.ico_size_update.x, self.ico_size_update.y)
        self.pic_4.setIcon(QIcon("assets/btnSet/btn_4.png"))
        self.pic_4.setIconSize(QSize(500, 500))
        self.pic_4.setStyleSheet(btn_style)

        self.return_to_menu = AnimatedButton('', self)
        # set button position & size
        self.return_to_menu.setGeometry(update_pos[5].x, update_pos[5].y, self.re_size_update.x, self.re_size_update.y)
        self.return_to_menu.setIcon(QIcon("assets/btnSet/ico.png"))
        self.return_to_menu.setIconSize(QSize(self.return_to_menu.width(), self.return_to_menu.height()))
        self.return_to_menu.setStyleSheet(menu_style)
        self.return_to_menu.setVisible(False)

        self.pic_0.clicked.connect(self.pic_0_Clicked)
        self.pic_1.clicked.connect(self.pic_1_Clicked)
        self.pic_2.clicked.connect(self.pic_2_Clicked)
        self.pic_3.clicked.connect(self.pic_3_Clicked)
        self.pic_4.clicked.connect(self.pic_4_Clicked)

        # If press, change ico; if release, return to menu
        self.return_to_menu.pressed.connect(self.change_icon_on_press)
        self.return_to_menu.released.connect(self.return_to_Menu)

        # create a label to play video
        self.video_label = QLabel(self)
        #set geometry as full window
        self.video_label.setGeometry(self.rect())
        self.video_label.setAttribute(Qt.WA_TransparentForMouseEvents,True)
        self.video_label.setVisible(False)
        self.video_label.setScaledContents(True)
        self.video_label.stackUnder(self.return_to_menu)

        self.label_btn=QLabel(self)
        self.label_btn.setGeometry(update_pos[5].x, 500, self.re_size_update.x, self.re_size_update.y)
        self.label_btn.setPixmap(QPixmap("assets/btnSet/ico.png"))
        self.label_btn.setScaledContents(True)
        self.label_btn.setStyleSheet("background-color: transparent;")
        self.label_btn.setAttribute(Qt.WA_TransparentForMouseEvents,True)  #set label do not interferce click

        #set label_btn opacity to 0
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0)
        self.return_to_menu.setGraphicsEffect(self.opacity_effect)
        self.label_btn.setGraphicsEffect(self.opacity_effect)

        #Qtimer for update frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        #QTimer for returnbutton
        # self.re_showTimer =QTimer()
        # self.re_showTimer.timeout.connect(self.return_show)

        # init audio source
        self.menu_au = QMediaPlayer()
        menu_au_url = QUrl.fromLocalFile('assets/Audio/menu_au.mp3')
        content_menu = QMediaContent(menu_au_url)
        self.menu_au.setMedia(content_menu)

        self.menuTimer = QTimer()
        self.menu_cy_Timer =QTimer()
        # menuTimer.setInterval(2000)
        # menuTimer.timeout.connect(self.menu_audio)

        self.menu_audio()


        self.return_intro = QMediaPlayer()
        return_intro_url_0 = QUrl.fromLocalFile('assets/Audio/return_au.mp3')
        content_return_intro = QMediaContent(return_intro_url_0)
        self.return_intro.setMedia(content_return_intro)

        self.btn_au = QMediaPlayer()
        btn_au_url_0 = QUrl.fromLocalFile('assets/Audio/button_au.mp3')
        content_btn_au = QMediaContent(btn_au_url_0)
        self.btn_au.setMedia(content_btn_au)

        self.au_0 = QMediaPlayer()
        au_url_0 = QUrl.fromLocalFile('assets/Audio/au_0.mp3')
        content_0 = QMediaContent(au_url_0)
        self.au_0.setMedia(content_0)

        self.au_1 = QMediaPlayer()
        au_url_1 = QUrl.fromLocalFile('assets/Audio/au_1.mp3')
        content_1 = QMediaContent(au_url_1)
        self.au_1.setMedia(content_1)

        self.au_2 = QMediaPlayer()
        au_url_2 = QUrl.fromLocalFile('assets/Audio/au_2.mp3')
        content_2 = QMediaContent(au_url_2)
        self.au_2.setMedia(content_2)

        self.au_3 = QMediaPlayer()
        au_url_3 = QUrl.fromLocalFile('assets/Audio/au_3.mp3')
        content_3 = QMediaContent(au_url_3)
        self.au_3.setMedia(content_3)

        self.au_4 = QMediaPlayer()
        au_url_4 = QUrl.fromLocalFile('assets/Audio/au_4.mp3')
        content_4 = QMediaContent(au_url_4)
        self.au_4.setMedia(content_4)


    def resizeEvent(self, event):
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        # whether press Escape
        if event.key() == Qt.Key_Escape:
            self.close()  # if pressed , close the window

    def pic_0_Clicked(self):
        # print("pic_0 clicked!")
        self.pic_0.setVisible(False)
        self.pic_1.setVisible(False)
        self.pic_2.setVisible(False)
        self.pic_3.setVisible(False)
        self.pic_4.setVisible(False)
        # self.return_to_menu.setVisible(True)
        self.btn_au.play()
        self.menu_au.stop()
        QTimer.singleShot(500, lambda: self.return_to_menu.setVisible(True))
        # self.OutIn_return_anim(self,0,1)
        self.play_video_0()

    def pic_1_Clicked(self):
        # print("pic_0 clicked!")
        self.pic_0.setVisible(False)
        self.pic_1.setVisible(False)
        self.pic_2.setVisible(False)
        self.pic_3.setVisible(False)
        self.pic_4.setVisible(False)

        self.btn_au.play()
        self.menu_au.stop()
        QTimer.singleShot(500, lambda: self.return_to_menu.setVisible(True))
        self.play_video_1()

    def pic_2_Clicked(self):
        self.pic_0.setVisible(False)
        self.pic_1.setVisible(False)
        self.pic_2.setVisible(False)
        self.pic_3.setVisible(False)
        self.pic_4.setVisible(False)

        self.btn_au.play()
        self.menu_au.stop()
        QTimer.singleShot(500, lambda: self.return_to_menu.setVisible(True))
        self.play_video_2()

    def pic_3_Clicked(self):
        self.pic_0.setVisible(False)
        self.pic_1.setVisible(False)
        self.pic_2.setVisible(False)
        self.pic_3.setVisible(False)
        self.pic_4.setVisible(False)

        self.btn_au.play()
        self.menu_au.stop()
        QTimer.singleShot(500, lambda: self.return_to_menu.setVisible(True))
        self.play_video_3()

    def pic_4_Clicked(self):
        self.pic_0.setVisible(False)
        self.pic_1.setVisible(False)
        self.pic_2.setVisible(False)
        self.pic_3.setVisible(False)
        self.pic_4.setVisible(False)

        self.btn_au.play()
        self.menu_au.stop()
        QTimer.singleShot(500, lambda: self.return_to_menu.setVisible(True))
        self.play_video_4()

    def return_to_Menu(self):
        print("menu is pressed")

        self.return_to_menu.setIcon(QIcon("assets/btnSet/ico.png"))
        #stop video playing

        self.pic_0.setVisible(True)
        self.pic_1.setVisible(True)
        self.pic_2.setVisible(True)
        self.pic_3.setVisible(True)
        self.pic_4.setVisible(True)
        # self.return_to_menu.setVisible(False)
        QTimer.singleShot(80, lambda: self.return_to_menu.setVisible(False))
        #stop video & audio, play menu audio
        self.stop_video()
        self.stop_audio()
        self.menu_au_play()


    def menu_au_play(self):
        self.menu_au.play()
        print("menu_au is playing")

    def change_icon_on_press(self):
        self.return_intro.play()
        self.return_to_menu.setIcon(QIcon("assets/btnSet/pressed_ico.png"))

    def OutIn_return_anim(self, begin_opcacity, end_opacity):

        self.OutIn_return_anim = QPropertyAnimation(self.opacity_effect,b"opacity")
        self.OutIn_return_anim.setDuration(1000)
        self.OutIn_return_anim.setEndValue(QEasingCurve.OutCurve)
        self.OutIn_return_anim.setStartValue(begin_opcacity)
        self.OutIn_return_anim.setEndValue(end_opacity)
        self.OutIn_return_anim.start()

    def start_0_animation(self):

        rect = QSizeF(320 * self.resolution,320 * self.resolution)
        shrink = QSizeF(280 * self.resolution,280 * self.resolution)
        self.animation_0 = QPropertyAnimation(self.pic_0, b'iconSize')
        self.animation_0.setEasingCurve(QEasingCurve.OutInQuad)
        self.animation_0.setDuration(1200)
        self.animation_0.setStartValue(rect)
        self.animation_0.setKeyValueAt(0.3, shrink)  # 中间状态，缩小为原来的80%
        self.animation_0.setEndValue(rect)
        self.animation_0.setLoopCount(-1)  # 无限循环
        self.animation_0.start()

    def start_1_animation(self):
        # resolution = int(self.size().width()/self.des.x)
        # rect = QSize(320 * resolution,320 * resolution)
        # shrink = QSize(280 * resolution,280 * resolution)
        rect = QSizeF(320 * self.resolution,320 * self.resolution)
        shrink = QSizeF(280 * self.resolution,280 * self.resolution)
        self.animation_1 = QPropertyAnimation(self.pic_1, b'iconSize')
        self.animation_1.setEasingCurve(QEasingCurve.OutInQuad)
        self.animation_1.setDuration(1200)
        self.animation_1.setStartValue(rect)
        self.animation_1.setKeyValueAt(0.3, shrink)  # 中间状态，缩小为原来的80%
        self.animation_1.setEndValue(rect)
        self.animation_1.setLoopCount(-1)  # 无限循环
        self.animation_1.start()

    def start_2_animation(self):
        # resolution = (self.size().width()/self.des.x)
        # print(resolution)
        # rect = QSizeF(320 * resolution,320 * resolution)
        # shrink = QSizeF(280 * resolution,280 * resolution)

        rect = QSizeF(320 * self.resolution,320 * self.resolution)
        shrink = QSizeF(280 * self.resolution,280 * self.resolution)
        self.animation_2 = QPropertyAnimation(self.pic_2, b'iconSize')
        self.animation_2.setEasingCurve(QEasingCurve.OutInQuad)
        self.animation_2.setDuration(1200)
        self.animation_2.setStartValue(rect)
        self.animation_2.setKeyValueAt(0.3, shrink)  # shrink its size
        self.animation_2.setEndValue(rect)
        self.animation_2.setLoopCount(-1)  # 无限循环
        self.animation_2.start()

    def start_3_animation(self):
        rect = QSizeF(320 * self.resolution,320 * self.resolution)
        shrink = QSizeF(280 * self.resolution,280 * self.resolution)
        self.animation_3 = QPropertyAnimation(self.pic_3, b'iconSize')
        self.animation_3.setEasingCurve(QEasingCurve.OutInQuad)
        self.animation_3.setDuration(1200)
        self.animation_3.setStartValue(rect)

        self.animation_3.setKeyValueAt(0.3, shrink)  # 中间状态，缩小为原来的80%
        self.animation_3.setEndValue(rect)
        self.animation_3.setLoopCount(-1)  # 无限循环
        self.animation_3.start()

    def start_4_animation(self):
        rect = QSizeF(320 * self.resolution,320 * self.resolution)
        shrink = QSizeF(280 * self.resolution,280 * self.resolution)
        self.animation_4 = QPropertyAnimation(self.pic_4, b'iconSize')
        self.animation_4.setEasingCurve(QEasingCurve.OutInQuad)
        self.animation_4.setDuration(1200)
        self.animation_4.setStartValue(rect)

        self.animation_4.setKeyValueAt(0.3, shrink)  # 中间状态，缩小为原来的80%
        self.animation_4.setEndValue(rect)
        self.animation_4.setLoopCount(-1)  # 无限循环
        self.animation_4.start()

    def play_video_0(self):
        self.video_label.setVisible(True)
        self.au_0.play()

        self.cap = cv2.VideoCapture('assets/Video/video_0.mp4')
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return
        self.timer.start(30)  # Adjust frame rate as needed

    def play_video_1(self):
        self.video_label.setVisible(True)
        self.au_1.play()

        self.cap = cv2.VideoCapture('assets/Video/video_1.mp4')
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return
        self.timer.start(30)  # Adjust frame rate as needed

    def play_video_2(self):
        self.video_label.setVisible(True)
        self.au_2.play()

        self.cap = cv2.VideoCapture('assets/Video/video_2.mp4')
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return
        self.timer.start(30)  # Adjust frame rate as needed

    def play_video_3(self):
        self.video_label.setVisible(True)
        self.au_3.play()

        self.cap = cv2.VideoCapture('assets/Video/video_3.mp4')
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return
        self.timer.start(30)  # Adjust frame rate as needed

    def play_video_4(self):
        self.video_label.setVisible(True)
        self.au_4.play()

        self.cap = cv2.VideoCapture('assets/Video/video_4.mp4')
        if not self.cap.isOpened():
            print("Error: Unable to open video file.")
            return
        self.timer.start(30)  # Adjust frame rate as needed

    def stop_video(self):
        self.timer.stop()
        if hasattr(self, 'cap'):
            self.cap.release()
        self.video_label.setVisible(False)

    def stop_audio(self):
        #stop audio voice
        self.au_0.stop()
        self.au_1.stop()
        self.au_2.stop()
        self.au_3.stop()
        self.au_4.stop()

    def menu_audio(self):
        if self.pic_0.isVisible() == True :
            self.menu_au.play()
            #cycle reference to loop play
            self.menuTimer.singleShot(114000, lambda: self.menu_au_cycle())
        print("Audio started")

    def menu_au_cycle(self):
        self.menu_au.stop()
        self.menu_cy_Timer.singleShot(10, lambda :self.menu_audio())
        print("menu_cy_timer started")
        # self.menuTimer.start()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.menu_au.stop()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)
        else:
            self.timer.stop()
            self.cap.release()
            QTimer.singleShot(1300, lambda: self.stop_audio())
            self.video_label.setVisible(False)
            self.pic_0.setVisible(True)
            self.pic_1.setVisible(True)
            self.pic_2.setVisible(True)
            self.pic_3.setVisible(True)
            self.pic_4.setVisible(True)
            QTimer.singleShot(80, lambda: self.return_to_menu.setVisible(False))
            # if return to menu , then play menu au
            QTimer.singleShot(1500,lambda: self.menu_au.play() )
            print("Audio Plays Here")



if __name__ == '__main__':
    # # fit different resolution
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    window.show()
    sys.exit(app.exec_())
