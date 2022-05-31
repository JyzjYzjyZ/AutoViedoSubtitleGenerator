import sys;sys.path.append('./gui');sys.path.append('./VoiceRecognition_function_goodjin5')
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.Gui_mainWindow import StyleSheet
from gui.Gui_FramelessWindow_Frame import FramelessWindow
from gui.Gui_mainWindow import MainWindow
from gui import path_head as path_head
from gui import handle_Input_Start
import time
# from gui.Handle_ElementCreate import createElement
# --noconfirm


start = time.time()
app = QApplication(sys.argv)
app.setStyleSheet(StyleSheet)
w = FramelessWindow()
w.setTitleBarHeight(75)# 定值
w.setWindowIcon(QIcon(f'{path_head}/ui_svg/logo_x56.svg'))
mainWindow = MainWindow(w)
# 按钮命令绑定
mainWindow.ui.input_b.clicked.connect(
    lambda :handle_Input_Start.HandleInput(
        element= mainWindow.ui.input_b,
        MainWindow=mainWindow
    )
)
mainWindow.ui.switch_b.clicked.connect(lambda :handle_Input_Start.HandleStart())

# createElement(mainWindow,'00000000000')

w.setWidget(mainWindow)  # 把自己的窗口添加进来
w.show()
sys.exit(app.exec_())
print(time.time() - start)
