

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt



class Film_widget(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(str)

    def __init__(self, Form, layout, icon_url, name):
        super(Film_widget, self).__init__(parent=Form)
        self.setGeometry(QtCore.QRect(0, 0, 560, 236))
        self.setMaximumSize(560, 236)
        self.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.film_icon = QtWidgets.QLabel(parent=self)
        self.film_icon.setMinimumSize(QtCore.QSize(150, 236))
        self.film_icon.setStyleSheet("border-radius: 5px;\n"
"background-color: black;")
        self.film_icon.setText("")
        self.film_icon.setObjectName("film_icon")
        self.horizontalLayout.addWidget(self.film_icon)
        self.film_name = QtWidgets.QLabel(parent=self)
        self.film_name.setMinimumSize(QtCore.QSize(400, 236))
        self.film_name.setStyleSheet("color: white;\n"
"font-size: 18px;\n"
"font-family: \"cascadia code\";\n"
"padding: 10px;")
        self.film_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.film_name.setObjectName("film_name")
        self.horizontalLayout.addWidget(self.film_name)
        layout.addWidget(self)
        self.film_name.setText(name)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.set_image(icon_url)

    def set_image(self, icon_url):
        import requests
        try:
            icon_url = icon_url.replace("\\", "/") 
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            self.film_icon.setPixmap(pixmap)
            self.film_icon.setScaledContents(True)  
        except Exception as e:
            print(f"Error: {e}")
            self.film_icon.setStyleSheet("background-color: black;") 

    def mousePressEvent(self, event):
        self.clicked.emit(self.film_name.text())

            

class Session_widget(QtWidgets.QWidget):
    def __init__(self, Form, layout, date, type, times):
        super(Session_widget, self).__init__(parent=Form)
        self.setGeometry(QtCore.QRect(0, 0, 620, 50))
        self.setObjectName("widget")
        self.setStyleSheet("font-family: \"cascadia code\";\n"
                            "color: white;\n"
                            "font-size: 16px;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.date = QtWidgets.QLabel(parent=self)
        self.date.setMinimumSize(QtCore.QSize(250, 50))
        self.date.setMaximumSize(QtCore.QSize(250, 50))
        self.date.setStyleSheet("padding: 5px;\n"
                                "border-right: 2px solid white;")
        self.date.setObjectName("date")
        self.date.setText(date)
        self.horizontalLayout.addWidget(self.date)
        self.type = QtWidgets.QLabel(parent=self)
        self.type.setMinimumSize(QtCore.QSize(150, 50))
        self.type.setMaximumSize(QtCore.QSize(150, 50))
        self.type.setStyleSheet("padding: 5px;\n"
                                "border-right: 2px solid white;")
        self.type.setObjectName("type")
        self.type.setText(type)
        self.horizontalLayout.addWidget(self.type)
        self.times = QtWidgets.QLabel(parent=self)
        self.times.setMinimumSize(QtCore.QSize(200, 50))
        self.times.setMaximumSize(QtCore.QSize(16777215, 50))
        self.times.setStyleSheet("padding: 5px;")
        self.times.setObjectName("times")
        self.times.setText(f'{times}')
        self.horizontalLayout.addWidget(self.times)
        layout.addWidget(self)
        QtCore.QMetaObject.connectSlotsByName(Form)
