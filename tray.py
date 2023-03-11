from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from pynput import keyboard
import pyperclip
import pyautogui
import clipboard_file
from time import sleep

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
            "QListWidget::item:hover {background-color:rgba(198, 219, 249, 0.5);} QListWidget::item:selected {background-color:rgba(198, 219, 249, 0.5); color:#000000;}"
            + "QListWidget::item { padding-top: 10px; padding-bottom: 10px;}")
        self.widget.itemClicked.connect(self.Clicked)
        self.setCentralWidget(self.widget)

    def Clicked(self, item):
        clip = item.text()
        clipboard_file.ignore_clip(clip)
        pyperclip.copy(clip)
        print(f'paste: {clip}')
        self.hide()
        self.paste()

    def paste(self):
        controller = keyboard.Controller()
        with controller.pressed(keyboard.Key.cmd):
            controller.press('v')
            controller.release('v')

    def load_clipboard_history(self):
        self.widget.clear()
        items = clipboard_file.read_clipboard()
        for item in items:
            item = QListWidgetItem(item)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.widget.addItem(item)


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
    clip_history.load_clipboard_history()
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
