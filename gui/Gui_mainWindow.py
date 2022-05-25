#!/usr/bin/env python
# -*- coding: utf-8 -*-

StyleSheet = """
/*标题栏*/
TitleBar {
    background-color: rgb(196, 196, 196);
}

/*最小化最大化关闭按钮通用默认背景*/
#buttonMinimum,#buttonMaximum,#buttonClose {
    border: none;
    background-color: rgb(196, 196, 196);
}

/*悬停*/
#buttonMinimum:hover,#buttonMaximum:hover {
    background-color: rgb(243,152,0);
}
#buttonClose:hover {
    color: white;
    background-color: rgb(232, 17, 35);
}

/*鼠标按下不放*/
#buttonMinimum:pressed,#buttonMaximum:pressed {
    background-color: rgb(44, 125, 144);
}
#buttonClose:pressed {
    color: white;
    background-color: rgb(161, 73, 92);
}
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
try:
    from Gui_body import Ui_Form
    from Gui_Element_dataFrame import Element_data
    from Gui_FramelessWindow_Frame import FramelessWindow  # @UnresolvedImport
except:
    from .Gui_body import Ui_Form
    from .Gui_Element_dataFrame import Element_data
    from .Gui_FramelessWindow_Frame import FramelessWindow  # @UnresolvedImport
import gui

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.is_parents_have_element = False


        '''create'''

        miniFrame = QFrame()
        miniFrame.setMaximumWidth(1500)
        self.ui = Ui_Form()
        self.ui .setupUi(miniFrame)
        horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        '''set'''
        layout.addItem(horizontalSpacer_1)
        layout.addWidget(miniFrame)
        layout.addItem(horizontalSpacer_2)
        layout.setStretch(1,4)
        layout.setStretch(2,1)
        layout.setStretch(0,1)

        '''new var'''
        self.parentWidget = self.ui.scrollAreaWidget_body
        self.parentLayout = self.ui.scrollAreaWidget_body_vlayout


        '''set centence'''
        self.createElement('1111')
        self.createElement('3333')
        self.createElement('2222')
        self.createElement('4444')

        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.parentLayout.addSpacerItem(verticalSpacer)


    def createElement(self,path):
        SPACE_ELEMENT = 5
        def open():
            print(f'open --> :{path}')
        def play():
            print(f'play --> :{path}')
        element_data= Element_data(path,self.parentWidget)
        elementData  =   element_data.WidgetObj
        elementData_paddingLayout = QVBoxLayout(self.parentWidget)
        self.createElement_ShadowEffect(elementData)

        '''setFunc'''
        element_data.b_open.clicked.connect(open)
        element_data.b_play.clicked.connect(play)

        elementData_paddingLayout.addWidget(elementData)
        elementData_paddingLayout.setContentsMargins(
            SPACE_ELEMENT,
            int(SPACE_ELEMENT/2)+1 if self.is_parents_have_element else SPACE_ELEMENT,
            SPACE_ELEMENT,
            int(SPACE_ELEMENT/2))
        self.parentLayout.addLayout(elementData_paddingLayout)
        self.is_parents_have_element = True

    def createElement_ShadowEffect(self,Form:QWidget):
        effect_shadow = QGraphicsDropShadowEffect(Form)
        effect_shadow.setOffset(0, 0)
        effect_shadow.setBlurRadius(10)
        c = QColor(0,0,0)
        c.setAlpha(255)
        effect_shadow.setColor(c)
        Form.setGraphicsEffect(effect_shadow)

if __name__ == '__main__':


    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    w = FramelessWindow()
    w.setTitleBarHeight(75)# 定值
    w.setWindowIcon(QIcon(f'{gui.path_head}/ui_svg/logo_x56.svg'))
    w.setWidget(MainWindow(w))  # 把自己的窗口添加进来
    w.show()
    sys.exit(app.exec_())
