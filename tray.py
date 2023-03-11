from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from pynput import keyboard
import pyautogui

pyautogui.press('shift')

suppress = False


class hotkey_listener(QtCore.QObject):
    hotkey_pressed = QtCore.pyqtSignal()
    listen = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(hotkey_listener, self).__init__(parent)
        self.listen.connect(self.global_hotkeys)

    def on_activate_v(self):
        print("ctrl+v hotkey pressed!")
        if not suppress:
            self.hotkey_pressed.emit()

    def global_hotkeys(self):
        listener = keyboard.GlobalHotKeys({
            '<ctrl>+v': self.on_activate_v
        })
        listener.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        width = 300
        height = 400
        self.setFixedSize(width, height)
        self.setWindowTitle("Clipstory")
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.widget = QListWidget(self)
        self.widget.setMouseTracking(True)
        self.widget.setStyleSheet(
            "QListWidget::item:hover {background-color:rgba(198, 219, 249, 0.5);}")
        self.widget.addItems(["One", "Two", "Three"])
        self.setCentralWidget(self.widget)


def hideMacDockIcon():
    import AppKit
    NSApplicationActivationPolicyRegular = 0
    NSApplicationActivationPolicyAccessory = 1
    NSApplicationActivationPolicyProhibited = 2
    AppKit.NSApp.setActivationPolicy_(NSApplicationActivationPolicyProhibited)


app = QApplication([])
hideMacDockIcon()
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("icon.png")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

clip_history = MainWindow()


def show_clip_history():
    x, y = pyautogui.position()
    clip_history.move(x - 150, y - 50)
    clip_history.show()


listener = hotkey_listener()
listener.hotkey_pressed.connect(show_clip_history)
listener.listen.emit()
# Create the menu
menu = QMenu()
action = QAction("A menu item")
action.setShortcut(QKeySequence('Meta+v'))
action.triggered.connect(show_clip_history)
menu.addAction(action)

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec()
