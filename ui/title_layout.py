# -*- coding: utf-8 -*-
'''
author gj5
date 22.4.9
v 1.0
'''
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys




class Title_bar_ui_layout(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setObjectName('ui_title_bar')
        if __name__=="__main__":
            self.setStyleSheet('''*{border:1px solid #1d649c}QWidget#ui_title_bar{background-color:#c4c4c4}''')
        else:
            self.setStyleSheet('''QWidget#ui_title_bar{background-color:#c4c4c4}''')
        self.set_titleLayout()
        self.resize(
        900,96)


    def set_titleLayout(self):
        '''set title bar'''

        '''create main layout  <|||>'''
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)


        '''create logo and background <pix & bg-image>'''
        svg_layout = QHBoxLayout()
        svg_layout.setSpacing(0)
        # svg_layout.setContentsMargins(0,0,0,0)
        svg_layout.setContentsMargins(46,5,6,4)

        svg = QLabel(self)
        svg.setPixmap(QPixmap('./ui_svg/logo_x64.svg'))
        svg.setObjectName('svg')
        svg.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        svg.setStyleSheet('''QFrame#svg{
            background-image: url('ui_svg/logo_background_circle_x96_EDEDED.svg');
            background-repeat: no-repeat;
            background-position: center center;
            
            padding: 16px
            }''')
        # self.svg = svg
        
        
        '''create text font'''
        font_introduce = QFont()
        try:
            font_introduce.setFamily(u"Source Han Sans CN")
        except:pass
        font_introduce.setPointSize(16)
        font_introduce.setBold(False)
        font_introduce.setWeight(50)
        
        '''create text <==>'''
        introuduceLayout = QVBoxLayout()
        introuduceLayout.setSpacing(5)
        introuduceLayout.setContentsMargins(0,0,0,0)
        line1 = QLabel()
        line1.setText(QCoreApplication.translate("Form",u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">G</span><span style=\" font-size:16pt;\">oodjin5's-</span><span style=\" font-size:16pt; font-weight:600;\">A</span><span style=\" font-size:16pt;\">uto-</span><span style=\" font-size:16pt; font-weight:600;\">S</span><span style=\" font-size:16pt;\">ubtitle-</span><span style=\" font-size:16pt; font-weight:600;\">G</span><span style=\" font-size:16pt;\">enerator</span></p></body></html>",None))
        line2 = QLabel()
        line2.setText(QCoreApplication.translate("Form","<html><head/><body><p><span style=\" font-size:16pt;\">Free Easy stabilization  off-line</span></p></body></html>",None))
        line1.setAlignment(Qt.AlignLeft|Qt.AlignBottom)
        line2.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        line1.setMargin(0)
        line2.setMargin(0)
        line1.setFont(font_introduce)
        line2.setFont(font_introduce)
        introuduceLayout.addWidget(line1)
        introuduceLayout.addWidget(line2)


        '''add to main'''
        svg_layout.addWidget(svg)
        right_horizontalSpacer = QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        mainLayout.addLayout(svg_layout)
        mainLayout.addLayout(introuduceLayout)
        mainLayout.addItem(right_horizontalSpacer)

if __name__=='__main__':
    app = QApplication(sys.argv)
    t =  Title_bar_ui_layout()
    t.show()
    sys.exit(app.exec_())
