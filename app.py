from tkinter import Tk, Label, ttk, Frame, BOTH
import clipboard_file
import pyautogui
import pyperclip

pyautogui.press('shift')

x, y = pyautogui.position()


def process_clipping(cliptext):
    cliptextCleaned = clean_clip_text(cliptext=cliptext)
    add_label(cliptextCleaned)


def clean_clip_text(cliptext):
    cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
    return cliptext


def on_click(labelElem):
    labelText = labelElem["text"]
    print(f'paste: {labelText}')
    clipboard_file.ignore_clip(labelText)
    pyperclip.copy(labelText)
    pyautogui.hotkey('command', 'tab')
    pyautogui.hotkey('command', 'v')
    root.destroy()


def on_hover(label):
    default_color = label["background"]
    label.bind("<Enter>", func=lambda e: label.config(background="#555555"))
    label.bind("<Leave>", func=lambda e: label.config(
        background=default_color))


def add_label(cliptext):
    frame = Frame(root, relief='sunken', bg="#555555")
    frame.pack(fill=BOTH, expand=True, padx=0, pady=0)

    label = Label(root, text=cliptext, cursor="pointinghand",
                  pady=5, padx=20, wraplength=400, width=40)
    label.bind(f"<Button-1>",
               lambda event, labelElem=label: on_click(labelElem))

    on_hover(label)
    label.pack()


def load_clip_history():
    clip_history = clipboard_file.read_clipboard()[::-1]
    for clip in clip_history:
        add_label(clip.strip())


if __name__ == '__main__':
    root = Tk()
    root.title("Clipstory")
    root.resizable(False, False)
    root.geometry(f'+{x - 200}+{y - 200}')
    load_clip_history()
    root.mainloop()
