from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from pynput import keyboard
import pyperclip
import pyautogui
import clipboard_file
from time import sleep
import os
import logging
from clipboard_listener import clipboard_listener

# TODO: pyinstaller / py2app are both buggy, just make install.sh?
listener = clipboard_listener()
listener.new_thread()

basedir = os.path.dirname(__file__)

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)


pyautogui.press('shift')

suppress = False


class hotkey_listener(QtCore.QObject):
    hotkey_pressed = QtCore.pyqtSignal()
    listen = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(hotkey_listener, self).__init__(parent)
        self.listen.connect(self.global_hotkeys)

    def on_activate_v(self):
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
        self.widget.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.widget.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.setCentralWidget(self.widget)

    def Clicked(self, item):
        setActivationPolicy(2)
        sleep(0.1)
        clip = item.text()
        clipboard_file.ignore_clip(clip)
        pyperclip.copy(clip)
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


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clipstory Settings")
        # Settings Values
        self.settings = clipboard_file.read_settings(
        ) or {'max_input_value': 20, 'save_history_across_sessions': False}
        self.max_input_value = self.settings['max_input_value']
        self.save_history_across_sessions = self.settings['save_history_across_sessions']

        # Save/Cancel buttons
        QBtn = QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        settings_box = QGroupBox()
        settings_layout = QVBoxLayout()

        # Set max history count
        max_label = QLabel("Max clipboard history count")
        max_input = QLineEdit()
        max_input.setMaxLength(2)
        max_input.setInputMask('00;')
        max_input.setText(str(self.max_input_value))
        max_input.setPlaceholderText("default: 20")
        max_input.textChanged.connect(self.max_input_changed)

        # Save history across sessions
        check = QCheckBox("Save history across sessions")
        check.setChecked(self.save_history_across_sessions)
        check.stateChanged.connect(self.save_history_across_sessions_changed)
        settings_layout.addWidget(max_label)
        settings_layout.addWidget(max_input)
        settings_layout.addWidget(check)
        settings_box.setLayout(settings_layout)

        self.layout = QVBoxLayout()
        self.layout.addWidget(settings_box)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def max_input_changed(self, s):
        if s == "":
            return
        self.max_input_value = int(s)

    def save_history_across_sessions_changed(self, s):
        self.save_history_across_sessions = s == 2

    def accept(self):
        setActivationPolicy(2)
        settings = {
            'max_input_value': self.max_input_value,
            'save_history_across_sessions': self.save_history_across_sessions
        }
        clipboard_file.save_settings(settings)
        return super().accept()

    def reject(self) -> None:
        setActivationPolicy(2)
        return super().reject()


def setActivationPolicy(policy):
    import AppKit
    NSApplicationActivationPolicyRegular = 0
    NSApplicationActivationPolicyAccessory = 1
    NSApplicationActivationPolicyProhibited = 2
    AppKit.NSApp.setActivationPolicy_(policy)


app = QApplication([])
setActivationPolicy(2)
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon(os.path.join(basedir, "icons", "icon.png"))

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

clip_history = MainWindow()


def show_clip_history():
    setActivationPolicy(1)
    x, y = pyautogui.position()
    clip_history.load_clipboard_history()
    clip_history.move(x - 150, y - 50)
    clip_history.show()
    clip_history.raise_()
    clip_history.activateWindow()


settings_dialog = SettingsDialog()


def show_options():
    setActivationPolicy(1)
    settings_dialog.show()
    settings_dialog.raise_()
    settings_dialog.activateWindow()


def quit_application():
    pyperclip.copy('CLIPSTORY:EVENT:CLOSE$')
    app.quit()


listener = hotkey_listener()
listener.hotkey_pressed.connect(show_clip_history)
listener.listen.emit()
# Create the menu
menu = QMenu()
action = QAction("Clipboard History")
action.setShortcut(QKeySequence('Meta+v'))
action.triggered.connect(show_clip_history)
menu.addAction(action)

options = QAction("Settings")
options.triggered.connect(show_options)
menu.addAction(options)

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(quit_application)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec()
