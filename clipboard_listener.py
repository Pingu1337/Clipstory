import pyperclip


class clipboard_listener:
    def __init__(self):
        self.content = pyperclip.paste()
        self.history = []

    # TODO: compare performance when triggered on ctrl-v keypress instead of clipboard polling
    def listen(self, processClipping):
        clipboard_content = pyperclip.paste()
        if (clipboard_content != self.content):
            self.content = clipboard_content
            self.history.append(clipboard_content)
            processClipping(cliptext=self.content)
