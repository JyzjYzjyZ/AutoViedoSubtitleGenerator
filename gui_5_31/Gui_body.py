# -*- coding: utf-8 -*-
import warnings,os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import gui
# from PyQt5.QtCore import pyqtSignal
'''229 ==> button'''
class ui_button_with_shadow():
    def _createElement_ShadowEffect(self,Form:QWidget,color,alpha,radius,offset):
        effect_shadow = QGraphicsDropShadowEffect(Form)
        effect_shadow.setOffset(offset[0],offset[1])
        effect_shadow.setBlurRadius(radius)
        c = QColor(color[0],color[1],color[2])
        c.setAlpha(alpha)
        effect_shadow.setColor(c)
        Form.setGraphicsEffect(effect_shadow)

    def _changeToOpacity(self, Form: QPushButton,Alpha=0):
        opacity = QtWidgets.QGraphicsOpacityEffect()
        opacity.setOpacity(Alpha)
        Form.setGraphicsEffect(opacity)


    Use_backgroundTransparent = True

    def _setNoneBackgroung(self,Element):
        if self.Use_backgroundTransparent == False:
            return
        Element.setStyleSheet('background:transparent;')

    def __init__(self,
                 pixmap_path:str,Form:QFrame=None,
                 color=[0,0,0],alpha=127,radius=10,offset=[0,0],
                 Margins_ui=0,
                Margins_button_hitbox = 0,
                 pixSize = [-1,-1],
                 ):
        '''
        :param pixmap_path: Image path of the button icon
        :param Form:Parent framework: Typically Widgets or Farme
        :param color:Lists 0-255 in RGB color
        :param alpha:Lists 0-255 in RGB color
        :param radius:Lists 0-255 in RGB color
        :param offset:Offset: Shadow offset accepts int list - >[x,y]
        '''
        '''
        按钮图标的图片路径 
        父级框架:一般为Widgets或Farme 
        颜色为rgb的列表0-255 
        透明度：0-255 
        阴影模糊半径 
        偏移：阴影偏移接受int列表->【x,y】 
        '''

        try:
            self.FrameObj = QFrame(Form)
        except:
            self.FrameObj = QFrame()
        self._setNoneBackgroung(self.FrameObj)
        # if __name__=='__main__':
        #     self.FrameObj.setStyleSheet('*{border:1px solid #ff0000}')
        self.FrameObj.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        glayout = QGridLayout(self.FrameObj)
        glayout.setSpacing(0)
        glayout.setContentsMargins(Margins_ui,Margins_ui,Margins_ui,Margins_ui)
        self.label  = QLabel(self.FrameObj)
        self._setNoneBackgroung(self.label)
        # if __name__=='__main__':
        #     self.label.setStyleSheet('*{border:1px solid #00ff00}')
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        if pixSize == [-1,-1]:
            self.Pix = QPixmap(pixmap_path)
        else:
            self.Pix = QPixmap(pixmap_path)
            try:
                self.Pix = self.Pix.scaled(pixSize[0],pixSize[1],Qt.KeepAspectRatio, Qt.SmoothTransformation)
            except:
                warnings.warn('pixSize:list ->[x,y]      x,y ->int')
        self.label.setPixmap(self.Pix)
        self.label.setAlignment(Qt.AlignCenter)
        self._createElement_ShadowEffect(self.label,color,alpha,radius,offset)
        glayout_for_button = QGridLayout(self.label)
        glayout_for_button.setSpacing(0)
        glayout_for_button.setContentsMargins(Margins_button_hitbox,Margins_button_hitbox
                                              ,Margins_button_hitbox,Margins_button_hitbox)
        self.button = QPushButton(self.label)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._changeToOpacity(self.button)
        self._setNoneBackgroung(self.button)
        glayout_for_button.addWidget(self.button)
        self.FrameObj.setProperty('class','button_ui')
        glayout.addWidget(self.label)

    def addText(self,From,FromLayout=None,Text='Test Text',font=None,
                Margins_element=0,
                Space_element=0,
                ):
        self.addTextObj = QWidget(From)
        self.addText_layout = QVBoxLayout(self.addTextObj)
        self.label_text = QLabel(self.addTextObj)
        self.label_text.setText(Text)


        self.addText_layout.setSpacing(Space_element)
        self.addText_layout.setContentsMargins(Margins_element,Margins_element,Margins_element,Margins_element)
        self.addText_layout.addWidget(self.FrameObj)
        self.addText_layout.addWidget(self.label_text)
        self.label_text.setAlignment(Qt.AlignCenter)

        try:
            self.label_text.setFont(font)
        except:
            if font == None:
                pass
            else:
                warnings.warn('The font you entered is not available', UserWarning)
        try:
            FromLayout.addWidget(self.addTextObj,2)
        except:
            if FromLayout == None:
                pass
            else:
                warnings.warn('please input obj>type=QxxxLayout',UserWarning)

        return self







class Ui_Form(object):


    def changeToOpacity(self,Form:QPushButton):
        opacity = QtWidgets.QGraphicsOpacityEffect()
        opacity.setOpacity(0.0)
        Form.setGraphicsEffect(opacity)

    def setUI_button_Shadow(self,Form):
        effect_shadow = QGraphicsDropShadowEffect(Form)
        effect_shadow.setOffset(0, 0)
        effect_shadow.setBlurRadius(10)
        c = QColor(0, 255, 0)
        c.setAlpha(255)
        effect_shadow.setColor(c)
        Form.setGraphicsEffect(effect_shadow)

    def setupUi(self, Form):
        StyleSheet = ''''''

        # Form.setStyleSheet('background-color:#ffffff')
        if not Form.objectName():
            Form.setObjectName(u"Form")
        # Form.setStyleSheet(u"*{border:1px solid #1d649c}")
        Form.setStyleSheet(
        # '''
        # .button_ui{
        #     border:1px solid #1d649c
        # }
        # '''
                           StyleSheet
                           )
        self.Main_vlayout = QVBoxLayout(Form)
        self.Main_vlayout.setSpacing(0)
        self.Main_vlayout.setObjectName(u"Main_vlayout")
        self.Main_vlayout.setContentsMargins(50, 70, 50, 45)
        self.header = QFrame(Form)
        self.header.setObjectName(u"header")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setFrameShadow(QFrame.Raised)
        self.header_vlayout = QHBoxLayout(self.header)
        self.header_vlayout.setSpacing(20)
        self.header_vlayout.setObjectName(u"header_vlayout")
        self.header_vlayout.setContentsMargins(0, 0, 0, 0)
        self.header.setMaximumHeight(100) #<================
        self.header.setStyleSheet('background-color: rgb(237,237,237);')

        '''set some ui button'''
        # font
        font = QFont()
        font.setFamily(u"Source Han Sans CN")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        # set
        ShadowAdditionalParameter = {
            'color':[30,30,30],
            'alpha':110,
            'radius':20,
            'offset':[0,6],
            # test
            'Margins_ui': 0,
            'Margins_button_hitbox': 0,
            'pixSize': [72,72],
        }


        input_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/input.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'input',font)
        switch_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/switch.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'switch',font)
        remove_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/remove.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'remove',font)
        setting_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/settings.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'setting',font)
        engine_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/engine.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'engine',font)

        recognition_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/recognition.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'recognition',font)
        translate_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/translate.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'translate',font)
        help_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/help.svg',**ShadowAdditionalParameter)\
            .addText(self.header,self.header_vlayout,'help',font)

        #作为子线程回传的信号
        # input_class.button.signalResult = pyqtSignal(list)


        # input_class.button.clicked.connect(lambda :gui.handle_Input_Start.HandleInput(input_class.button))
        # help_class.button.clicked.connect(lambda :gui.ui_button_handle('help'))
        # translate_class.button.clicked.connect(lambda :gui.ui_button_handle('translate'))
        # recognition_class.button.clicked.connect(lambda :gui.ui_button_handle('recognition'))
        # setting_class.button.clicked.connect(lambda :gui.ui_button_handle('setting'))
        # remove_class.button.clicked.connect(lambda :gui.ui_button_handle('remove'))
        # switch_class.button.clicked.connect(lambda :gui.handle_Input_Start.HandleStart())
        # engine_class.button.clicked.connect(lambda :gui.ui_button_handle('engine'))

        self.input_b = input_class.button
        self.help_b = help_class.button
        self.translate_b = translate_class.button
        self.recognition_b = recognition_class.button
        self.setting_b = setting_class.button
        self.remove_b = remove_class.button
        self.switch_b = switch_class.button
        self.engine_b = engine_class.button




        self.Main_vlayout.addWidget(self.header)

        self.verticalSpacer_in_middle = QSpacerItem(20, 66, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.Main_vlayout.addItem(self.verticalSpacer_in_middle)

        self.body = QFrame(Form)
        self.body.setObjectName(u"body")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy4)
        self.body.setFrameShape(QFrame.StyledPanel)
        self.body.setFrameShadow(QFrame.Raised)
        self.body_vlayout = QVBoxLayout(self.body)
        self.body_vlayout.setSpacing(0)
        self.body_vlayout.setObjectName(u"body_vlayout")
        self.body_vlayout.setContentsMargins(0, 0, 0, 0)
        self.body_top = QFrame(self.body)
        self.body_top.setObjectName(u"body_top")
        self.body_top.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.body_top.setMinimumHeight(40)
        self.body_top.setStyleSheet('background-color:rgb(104, 104, 104)')

        self.body_vlayout.addWidget(self.body_top)

        self.scrollArea_body = QScrollArea(self.body)
        self.scrollArea_body.setObjectName(u"scrollArea_body")
        self.scrollArea_body.setWidgetResizable(True)
        self.scrollAreaWidget_body = QWidget()
        # self.scrollAreaWidget_body.setObjectName(u"scrollAreaWidget_body")
        self.scrollAreaWidget_body.setGeometry(QRect(0, 0, 1093, 372))
        self.scrollAreaWidget_body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scrollAreaWidget_body_vlayout = QVBoxLayout(self.scrollAreaWidget_body)
        self.scrollAreaWidget_body_vlayout.setSpacing(0)
        self.scrollAreaWidget_body_vlayout.setObjectName(u"scrollAreaWidget_body_vlayout")
        self.scrollAreaWidget_body_vlayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_body.setProperty('class','is_scrollArea')
        self.scrollArea_body.setStyleSheet(
            '''
            .is_scrollArea{
            border:0px;
            }
            #Main_scrollAreaWidget_body{background:#C4C4C4;
            }
            
            QScrollArea QScrollBar:vertical{
                width: 18px;
                background:rgb(237, 237, 237); /*滚动条滑槽背景色*/
                padding-right:5px;
                padding-left:5px;
                padding-top:8px;
                padding-bottom:8px;
                border-radius:0px;
                }
            QScrollArea QScrollBar::handle:vertical{
                background:#C4C4C4;
                border-radius:4px;
                }
            QScrollArea QScrollBar::handle:vertical:hover{
                background:#F09428;
                border-radius:4px;
                }
            QScrollArea QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{
            background:transparent;border-radius:4px;
            }
            QScrollArea QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{
            height:0px;width:0px;
            }

            QScrollArea QScrollBar:horizontal{
                height: 10px;
                border-radius:4px;
                background:transparent;
                padding-bottom:2px;
                padding-left:5px;
                padding-right:5px;
                border-radius:4px;
                }
            QScrollArea QScrollBar::handle:horizontal{
                background:#C4C4C4;
                border-radius:4px;
                }
            QScrollArea QScrollBar::handle:horizontal:hover{
                background:#F09428;
                border-radius:4px;
                }
            QScrollArea QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{
            background:transparent;border-radius:4px;
            }
            QScrollArea QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{
            height:0px;width:0px;
            }
            '''
        )
        self.scrollAreaWidget_body.setObjectName('Main_scrollAreaWidget_body')
        self.scrollArea_body.setWidget(self.scrollAreaWidget_body)

        self.body_vlayout.addWidget(self.scrollArea_body)


        self.Main_vlayout.addWidget(self.body)

        self.Main_vlayout.setStretch(0, 6)
        self.Main_vlayout.setStretch(1, 3)
        self.Main_vlayout.setStretch(2, 26)# <==

        # self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi


    # retranslateUi

