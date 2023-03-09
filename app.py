from tkinter import Tk, Label, RAISED
from clipboard_listener import clipboard_listener
import pyperclip
listener = clipboard_listener()


def updateClipboard():
    listener.listen(processClipping=processClipping)
    root.after(ms=100, func=updateClipboard)


def processClipping(cliptext):
    cliptextCleaned = cleanClipText(cliptext=cliptext)
    # TODO: add new elements for each new item added to the clipboard history
    label["text"] = cliptextCleaned


def cleanClipText(cliptext):
    # Removing all characters > 65535 (that's the range for tcl)
    cliptext = "".join([c for c in cliptext if ord(c) <= 65535])
    return cliptext


def onClick(labelElem):
    labelText = labelElem["text"]
    print(listener.history)
    pyperclip.copy(labelText)


if __name__ == '__main__':
    root = Tk()
    label = Label(root, text="", cursor="plus",
                  relief=RAISED, pady=5,  wraplength=500)
    label.bind("<Button-1>", lambda event, labelElem=label: onClick(labelElem))
    label.pack()
    updateClipboard()
    root.mainloop()
