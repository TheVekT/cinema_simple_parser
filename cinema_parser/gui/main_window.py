import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QSize
from cinema_parser.gui.ui_mainwindow import Ui_MainWindow
from cinema_parser.gui.widgets import Film_widget, Session_widget
from cinema_parser.parser.main_parser import MovieParser
import asyncio
from qasync import QEventLoop, asyncSlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ініціалізація об'єкта інтерфейсу
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Планета кіно Parser")
        self.parsed_info = {}
        self.parser = MovieParser()
        self.ui.pushButton.clicked.connect(self.update_scroll_area)
        self.ui.pushButton2.clicked.connect(self.back)
      
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    sub_layout = item.layout()
                    if sub_layout is not None:
                        self.clear_layout(sub_layout)
                   
    def clear_children(self, obj, type):
        for child in obj.children():
            if isinstance(child, type):
                child.setParent(None)
                child.deleteLater()
                
    @asyncSlot()
    async def parse(self, url):
        self.parsed_info = await self.parser.parse_movie_sessions(url)
        await asyncio.sleep(0.2)
        self.parser.close()
        await asyncio.sleep(0.2)
        
    @asyncSlot()    
    async def update_scroll_area(self):
        self.clear_children(self.ui.scrollAreaWidgetContents, Film_widget)
        self.clear_layout(self.ui.verticalLayout_3)
        await self.parse("https://planetakino.ua/lviv-leo/showtimes/#month")
        for movie_name, movie_data in self.parsed_info.items():
            film_widget = Film_widget(
                self.ui.scrollAreaWidgetContents,
                self.ui.verticalLayout_3,
                movie_data["icon_url"], 
                movie_name 
            )
            
            film_widget.clicked.connect(self.update_tab2)
            await asyncio.sleep(0.1)
        
    def back(self):
        self.ui.pushButton2.hide()
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.lay1.setMaximumSize(QSize(550, 50))
   
    def update_tab2(self, film_name):
        self.clear_children(self.ui.scrollAreaWidgetContents_2, Session_widget)
        self.clear_layout(self.ui.verticalLayout_6)
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.pushButton2.show()
        self.ui.lay1.setMaximumSize(QSize(680, 50))
        for date, session in self.parsed_info[film_name]['sessions'].items():
            for type, times in session.items():
                film_session = Session_widget(self.ui.scrollAreaWidgetContents_2, self.ui.verticalLayout_6, date, type, times)
                
        