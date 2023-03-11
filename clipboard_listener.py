import pyperclip
import threading
import clipboard_file


class clipboard_listener:
    def __init__(self):
        self.content = pyperclip.paste()
        self.history = []
        self.thread = self.new_thread()

    def new_thread(self):
        next = threading.Thread(
            target=self.nextClip)
        next.start()
        return next

    def close(self):
        print('sending close event...')
        pyperclip.copy("CLIPSTORY:EVENT:CLOSE$")

    def nextClip(self):
        clipboard_content = pyperclip.waitForNewPaste()

        if (clipboard_content == "CLIPSTORY:EVENT:CLOSE$"):
            print('close event!')
            pyperclip.copy(self.content)
            return

        if (clipboard_content != self.content and not clipboard_file.ignored(clipboard_content) and clipboard_content != "" and clipboard_content != None):
            clipboard_content = "".join(
                [c for c in clipboard_content if ord(c) <= 65535])

            print(f'new copy: {clipboard_content}')

            self.content = clipboard_content
            self.history.append(clipboard_content)
            clipboard_file.append_clipboard(clipboard_content)
        self.new_thread()

    def read_from_file(self):
        self.history = clipboard_file.read_clipboard()
        return self.history
