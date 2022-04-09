# layout

```python
        button1 = QPushButton("Button One", self)
        button2 = QPushButton("Button Two", self)
        button3 = QPushButton("Button Two", self)

        vbox = QVBoxLayout()
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

        self.setLayout(vbox)
```

# Pixmap
```python
author_logo_background_pixmap = QtGui.QPixmap("./ui_svg/logo_background_circle.svg")
author_logo_background.setPixmap(author_logo_background_pixmap)
author_logo_background.setScaledContents(True)  # 图片自适应
```

# Align
```python
​​self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)​​
```

# Qss-background
```css
svg.setStyleSheet('''QFrame#svg{
            background-image: url('ui_svg/engine.svg');
            background-repeat: no-repeat;
            background-position: center center;
            }''')
```
# Layout Margins

```python
self.verticalLayout.setSpacing(0)
self.verticalLayout.setContentsMargins(0, 0, 0, 0)
```
# spacing
> 注意到：水平与竖直的**QSizePolicy**是不相同的这里我设置的是**MinimumExpanding**
```python
self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
```
# Margins
> left, top, right, bottom
# Qfont
```python
font1 = QFont()
        font1.setFamily(u"Source Han Sans CN")
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setWeight(50)

self.label_2.setFont(font1)
```
# encodeType
```python
# -*- coding: utf-8 -*-
```
