import sys;sys.path.append('./gui');sys.path.append('./VoiceRecognition_function_goodjin5')
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.Gui_mainWindow import StyleSheet
from gui.Gui_FramelessWindow_Frame import FramelessWindow
from gui.Gui_mainWindow import MainWindow
from gui import path_head as path_head


# --noconfirm



app = QApplication(sys.argv)
app.setStyleSheet(StyleSheet)
w = FramelessWindow()
w.setTitleBarHeight(75)# 定值
w.setWindowIcon(QIcon(f'{path_head}/ui_svg/logo_x56.svg'))
w.setWidget(MainWindow(w))  # 把自己的窗口添加进来
w.show()
sys.exit(app.exec_())