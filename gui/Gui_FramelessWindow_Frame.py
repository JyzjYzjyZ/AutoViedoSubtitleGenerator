#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Created on 2018年4月30日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: FramelessWindow
@description:
"""
import copy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QFont, QEnterEvent, QPainter, QColor, QPen,QIcon,QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QSpacerItem, QSizePolicy, QPushButton
import gui



class TitleBar(QWidget):
    # 窗口最小化信号
    windowMinimumed = pyqtSignal()
    # 窗口最大化信号
    windowMaximumed = pyqtSignal()
    # 窗口还原信号
    windowNormaled = pyqtSignal()
    # 窗口关闭信号
    windowClosed = pyqtSignal()
    # 窗口移动
    windowMoved = pyqtSignal(QPoint)

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)
        # 支持qss设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        # 设置幽灵图标
        self.iconLabel = QLabel()
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(255,255,255))
        self.setPalette(palette)
        '''按钮创建，self.button 不可改'''
        self.buttonMinimum = QPushButton('0', self, clicked=self.windowMinimumed.emit, objectName='buttonMinimum')
        self.buttonMaximum = QPushButton( '1', self, clicked=self.showMaximized, objectName='buttonMaximum')
        self.buttonClose = QPushButton('r', self, clicked=self.windowClosed.emit, objectName='buttonClose')

        self.BlurRadius = 10
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0.25)  # 偏移 <== 这个也需要微调
        self.effect_shadow.setBlurRadius(self.BlurRadius)  # 阴影半径
        self.ShadowColor = QColor(33,36,47) #k=52%
        self.ShadowColor.setAlpha(204)# A=80%
        self.effect_shadow.setColor(self.ShadowColor)  # 阴影颜色
        self.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中

        '''Style create'''
        main_hlayout = QHBoxLayout(self)
        main_hlayout.setContentsMargins(0,0,0,0)
        titleLayout = self.set_titleLayout(self)
        title_button = QHBoxLayout(self)
        title_button.setSpacing(0)
        '''add'''
        button_hlayout = QHBoxLayout(self)
        button_hlayout.setContentsMargins(0,0,0,0)
        button_hlayout.addWidget(self.buttonMinimum)
        button_hlayout.addWidget(self.buttonMaximum)
        button_hlayout.addWidget(self.buttonClose)
        '''set'''
        main_hlayout.addLayout(titleLayout)
        main_hlayout.addLayout(button_hlayout)





        # 初始高度
        self.setHeight()
    '''my func'''
    def set_titleLayout(self,Form):
        '''goodjin5'''
        '''set title bar'''
        # Form.setStyleSheet('*{border:1px solid #1d649c}')
        '''create main layout  <|||>'''
        mainLayout = QHBoxLayout(Form)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)


        '''create Shadow'''
        effect_shadow_svg = QGraphicsDropShadowEffect(self)
        effect_shadow_svg.setOffset(0, 6)  # 偏移
        effect_shadow_svg.setBlurRadius(6)  # 阴影半径
        shadow_color_svg = QColor(0,0,0)
        shadow_color_svg.setAlpha(32)
        effect_shadow_svg.setColor(shadow_color_svg)  # 阴影颜色

        effect_shadow_logo = QGraphicsDropShadowEffect(self)
        effect_shadow_logo.setOffset(0, 6)  # 偏移
        effect_shadow_logo.setBlurRadius(6)  # 阴影半径
        shadow_color_logo = QColor(0,0,0)
        shadow_color_logo.setAlpha(28)
        effect_shadow_logo.setColor(shadow_color_logo)  # 阴影颜色


        '''create logo and background <pix & bg-image>'''
        svg_layout = QHBoxLayout()
        svg_layout.setSpacing(0)
        # svg_layout.setContentsMargins(0,0,0,0)
        svg_layout.setContentsMargins(46, 0, 6, 0)

        svg = QLabel(Form)
        svg.setObjectName('svg')
        svg.setContentsMargins(0,0,0,0)
        svg.setPixmap(QPixmap(f'{gui.path_head}/ui_svg/logo_background_circle_x70_EDEDED.svg'))
        svg.setGraphicsEffect(effect_shadow_svg)
        svg_logo_layout = QGridLayout(svg)
        svg_logo_layout.setSpacing(0)
        svg_logo_layout.setContentsMargins(0,0,0,0)
        svg_logo = QLabel(svg)
        svg_logo.setObjectName('svg_logo')
        svg_logo.setPixmap(QPixmap(f'{gui.path_head}/ui_svg/logo_x50.svg'))
        svg_logo.setGraphicsEffect(effect_shadow_logo)
        svg_logo.setAlignment(Qt.AlignCenter)
        svg.setMinimumSize(75,75)
        svg_logo_layout.addWidget(svg_logo)


        '''create text font'''
        font_introduce = QFont()
        try:
            font_introduce.setFamily(u"Source Han Sans CN")
        except:
            pass
        font_introduce.setPointSize(16)
        font_introduce.setBold(False)
        font_introduce.setWeight(50)

        '''create text <==>'''
        introuduceLayout = QVBoxLayout()
        introuduceLayout.setSpacing(0)
        introuduceLayout.setContentsMargins(0, 0, 0, 0)
        line1 = QLabel()
        line1.setText(QCoreApplication.translate("Form",
                                                 u"<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">G</span><span style=\" font-size:16pt;\">oodjin5's-</span><span style=\" font-size:16pt; font-weight:600;\">A</span><span style=\" font-size:16pt;\">uto-</span><span style=\" font-size:16pt; font-weight:600;\">S</span><span style=\" font-size:16pt;\">ubtitle-</span><span style=\" font-size:16pt; font-weight:600;\">G</span><span style=\" font-size:16pt;\">enerator</span></p></body></html>",
                                                 None))
        line2 = QLabel()
        line2.setText(QCoreApplication.translate("Form",
                                                 "<html><head/><body><p><span style=\" font-size:16pt;\">Free Easy stabilization  off-line</span></p></body></html>",
                                                 None))
        line1.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        line2.setAlignment(Qt.AlignLeft | Qt.AlignTop)
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
        return  mainLayout




    def setIcon(self, icon):
        """设置图标"""
        self.iconLabel.setPixmap(icon.pixmap(64, 64))




    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # 最大化

            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # 还原

            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=38):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # 设置右边按钮的大小
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)


    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


# 枚举左上右下以及四个定点
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class FramelessWindow(QWidget):
    # 四周边距
    Margins = 10 #<== 这个值，谁改谁死

    def __init__(self, *args, **kwargs):
        super(FramelessWindow, self).__init__(*args, **kwargs)
        self._pressed = False
        self.Direction = None
        # 背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 鼠标跟踪
        self.setMouseTracking(True)
        # 布局
        layout = QVBoxLayout(self, spacing=0)
        # 预留边界用于实现无边框窗口调整大小
        layout.setContentsMargins(
            # 0,0,0,0)
            self.Margins, self.Margins, self.Margins, self.Margins)
        # 标题栏
        self.titleBar = TitleBar(self)
        layout.addWidget(self.titleBar)
        # 信号槽
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowIconChanged.connect(self.titleBar.setIcon)
        # 用户定义常量
        self.titleBarHeight = 38




    def _setTitleBarHeight(self,height):
        """设置标题栏高度"""
        self.titleBar.setHeight(height)

    def setTitleBarHeight(self,height=38):
        '''由于全屏时有margin不为0的标题栏布局上会有些许问题 需要手动扩大'''
        self.titleBarHeight = height
        self._setTitleBarHeight(height)

    def setWidget(self, widget):
        """设置自己的控件"""
        if hasattr(self, '_widget'):
            return
        color = QColor(44, 46, 58)
        color.setAlpha(153)
        Br = self.titleBar.BlurRadius
        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 2.2)  # 偏移  <== offset_Y 需要调整
        self.effect_shadow.setBlurRadius(Br)  # 阴影半径
        self.effect_shadow.setColor(color)  # 阴影颜色
        widget.setGraphicsEffect(self.effect_shadow)

        self._widget = widget
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(255,255,255))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            # 最大化或者全屏则不允许移动
            return
        super(FramelessWindow, self).move(pos)

    def showMaximized(self):
        """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
        self.effect_shadow.setBlurRadius(0)
        super(FramelessWindow, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._setTitleBarHeight(int(self.titleBarHeight+self.Margins))

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        self.effect_shadow.setBlurRadius(self.titleBar.BlurRadius)
        self._setTitleBarHeight(int(self.titleBarHeight))
        super(FramelessWindow, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)


    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(FramelessWindow, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
        super(FramelessWindow, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        super(FramelessWindow, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        '''鼠标弹起事件'''
        super(FramelessWindow, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        super(FramelessWindow, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # 左上角
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # 右下角
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # 右上角
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # 左下角
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # 左边
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # 右边
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # 上面
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # 下面
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        """调整窗口大小"""
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == LeftTop:  # 左上角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:  # 右下角
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:  # 右上角
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:  # 左下角
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:  # 左边
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:  # 右边
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:  # 上面
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:  # 下面
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)
