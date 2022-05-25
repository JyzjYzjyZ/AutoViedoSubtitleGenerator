from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import warnings,gui
try:
    from Gui_body import ui_button_with_shadow
except:
    from .Gui_body import ui_button_with_shadow

'''
显而易见 这是未完成版本
但是大差不差
'''



# def superButton(Form,StyleSheet:str,FrameShadow:QFrame.Shadow=QFrame.Plain):
#
#     return Fram,b


def sumDic(dic1:dict,dic2:dict):
    return dict(dic1,**dic2)



class Element_data():
    def openFile(self):
        print('openFile -> '+self.path)

    def playViedo(self):
        print('playViedo -> '+self.path)


    def __init__(self,path,Form:QWidget = None):
        try:
            # super(QWidget, self).__init__(Form)
            self.WidgetObj = QWidget(Form)
        except:
            # super(QWidget, self).__init__()
            self.WidgetObj = QWidget()
        self.WidgetObj.setObjectName('WidgetObj')

        self.path = path
        self.WidgetObj.setStyleSheet(
            r'''

            .is_scrollArea{
            border:0px;
            }
            
            .scrollWidget_element{
                background:#EDEDED
            }

            #WidgetObj{
                background:#EDEDED;
            }
            
            QScrollArea QScrollBar:vertical{
                width: 10px;
                background:transparent;
                padding-right:2px;
                padding-top:5px;
                padding-bottom:5px;
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
                border-radius:0px;
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
            # +
            # '*{border:1px solid #1d649c}'
        )
        # self.WidgetObj.setContentsMargins(100,20,30,40)# l t r b
        self.Create_element()
        if __name__ == '__main__':
            self.WidgetObj.show()

    def Create_element(self):
        '''Main'''
        self.MainLayout = QHBoxLayout(self.WidgetObj)
        self.MainLayout.setContentsMargins(15, 5, 10, 5)
        self.MainLayout.setSpacing(0)
        data_Layout = QHBoxLayout()

        '''Path'''
        scrollArea_dataPath = QScrollArea()
        scrollArea_dataPath.setProperty('class', 'is_scrollArea')
        scrollArea_dataPath.setWidgetResizable(True)
        scrollArea_dataPath.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        scrollArea_dataPath.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_dataPath_Widget = QWidget()
        scroll_dataPath_Widget.setProperty('class','scrollWidget_element')
        scroll_dataPath_Widget.setContentsMargins(0,0,0,0)
        scroll_dataPath_Widget_layout = QVBoxLayout(scroll_dataPath_Widget)
        dataPath_label = QLabel()
        dataPath_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        dataPath_label.setText(
            'PathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPathPath')
        # set max by label
        scrollArea_dataPath.setMaximumWidth(dataPath_label.width())
        # set
        scroll_dataPath_Widget_layout.addWidget(dataPath_label)
        scrollArea_dataPath.setWidget(scroll_dataPath_Widget)
        '''Imf'''
        scrollArea_dataImf = QScrollArea()
        scrollArea_dataImf.setProperty('class', 'is_scrollArea')
        scrollArea_dataImf.setWidgetResizable(True)
        scrollArea_dataImf.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        scrollArea_dataImf.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Expanding)
        scroll_dataImf_Widget = QWidget()
        scroll_dataImf_Widget.setProperty('class','scrollWidget_element')
        scroll_dataImf_Widget_layout = QVBoxLayout(scroll_dataImf_Widget)
        dataImf_label = QLabel()
        dataImf_label.setText(
            r'I222mf\nImf\nI')
        dataImf_label.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # set
        scroll_dataImf_Widget_layout.addWidget(dataImf_label)
        scrollArea_dataImf.setWidget(scroll_dataImf_Widget)


        '''preview'''
        preview = QLabel()
        preview.setText('PPPPPPPPPPPPPPPPPPVVVV')
        '''ui'''
        ShadowAdditionalParameter = {
            'color':[30,30,30],
            'alpha':100,
            'radius':4,
            'offset':[0,2],
        }
        SizeAdditionalParameter = {
            'Margins_ui':0,
            'Margins_button_hitbox':0,
            'pixSize':[40,40],
            # 如果图标宽度过宽 考虑是否是图标的问题
        }

        ui_VboxLayout = QVBoxLayout()
        ui_open_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/open_in_explorer.svg',self.WidgetObj,
                                              **sumDic(ShadowAdditionalParameter,SizeAdditionalParameter))
        ui_play_class = ui_button_with_shadow(f'{gui.path_head}/ui_svg/preview.svg',self.WidgetObj,
                                              **sumDic(ShadowAdditionalParameter,SizeAdditionalParameter))
        ui_open = ui_open_class.FrameObj
        self.b_open = ui_open_class.button
        ui_play = ui_play_class.FrameObj
        self.b_play = ui_play_class.button


        ui_VboxLayout.addWidget(ui_play)
        ui_VboxLayout.addWidget(ui_open)
        '''set'''''
        data_Layout.addWidget(scrollArea_dataImf,1)
        data_Layout.addWidget(scrollArea_dataPath,9999)
        data_Layout.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.MainLayout.addWidget(preview)
        self.MainLayout.addLayout(ui_VboxLayout)
        self.MainLayout.addLayout(data_Layout)

        self.WidgetObj.setSizePolicy(QSizePolicy.Preferred ,QSizePolicy.Fixed)
        # self.WidgetObj.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        # self.WidgetObj.setAlignment(Qt.AlignLeft|Qt.AlignTop)




# APP = QApplication([])
# e = Element_data('./ui_svg/preview.svg')
# print(type(e))
# print(type(e.WidgetObj))
# APP.exec_()