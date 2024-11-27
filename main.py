import sys
from PyQt6.QtWidgets import QApplication
from cinema_parser.gui.main_window import MainWindow
import asyncio
from qasync import QEventLoop




if __name__ == "__main__":
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    with loop:
        sys.exit(loop.run_forever())