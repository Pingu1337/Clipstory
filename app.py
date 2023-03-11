from tkinter import Tk, Frame, BOTH, Label
from pynput import keyboard
import clipboard_file
import pyautogui
import pyperclip
import time

pyautogui.press('shift')


class App():
    def __init__(self):
        self.root = Tk()
        self.inner = self.new_inner_frame()
        self.labels = []
        self.suppress = False

    def init(self):
        self.root.title("Clipstory")
        self.root.resizable(False, False)
        self.root.withdraw()
        self.root.mainloop()

    def new_inner_frame(self):
        inner = Frame(self.root)
        inner.pack()
        return inner

    def add_label(self, cliptext):
        frame = Frame(self.inner, relief='sunken', bg="#555555")
        frame.pack(fill=BOTH, expand=True, padx=0, pady=0)
        self.labels.append(frame)

        label = Label(self.inner, text=cliptext, cursor="pointinghand",
                      pady=5, padx=20, wraplength=400, width=40)

        label.bind(f"<Button-1>", lambda event,
                   labelElem=label: self.on_click(labelElem))

        self.on_hover(label)
        label.pack()
        self.labels.append(label)

    def load_clip_history(self):
        clip_history = clipboard_file.read_clipboard()[::-1]
        for clip in clip_history:
            self.add_label(clip.strip())

    def on_click(self, labelElem):
        self.suppress = True
        labelText = labelElem["text"]
        print(f'paste: {labelText}')
        clipboard_file.ignore_clip(labelText)
        pyperclip.copy(labelText)
        self.paste()
        self.hide()

    def paste(self):
        controller = keyboard.Controller()
        with controller.pressed(keyboard.Key.cmd):
            controller.press(keyboard.Key.tab)
            controller.release(keyboard.Key.tab)
        time.sleep(0.1)
        with controller.pressed(keyboard.Key.cmd):
            controller.press('v')
            controller.release('v')

    def on_hover(self, label):
        default_color = label["background"]
        label.bind("<Enter>", func=lambda e: label.config(
            background="#555555"))
        label.bind("<Leave>", func=lambda e: label.config(
            background=default_color))

    def show(self):
        x, y = pyautogui.position()
        self.root.geometry(f'+{x - 200}+{y - 100}')
        self.load_clip_history()
        self.root.update()
        self.root.deiconify()

    def hide(self):
        self.clear()
        self.root.update()
        self.root.withdraw()
        self.suppress = False

    def clear(self):
        for label in self.labels:
            label.destroy()


keys = []


def on_activate_v():
    if not app.suppress:
        app.show()


def global_hotkeys():
    listener = keyboard.GlobalHotKeys({
        '<ctrl>+v': on_activate_v
    })
    listener.start()


if __name__ == '__main__':
    app = App()
    global_hotkeys()
    app.init()
