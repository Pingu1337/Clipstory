import pyperclip
import threading
import clipboard_file


class clipboard_listener:
    def __init__(self):
        self.settings = clipboard_file.read_settings(
        ) or {'max_input_value': 20, 'save_history_across_sessions': False}
        self.max_input_value = self.settings['max_input_value']
        self.setup()
        self.content = pyperclip.paste()
        self.history = []

    def setup(self):
        if self.settings is not None:
            if not self.settings['save_history_across_sessions']:
                clipboard_file.clear_clipboard()

    def new_thread(self):
        next = threading.Thread(
            target=self.nextClip, name="NextClip")
        next.start()
        return next

    def close(self):
        pyperclip.copy("CLIPSTORY:EVENT:CLOSE$")

    def nextClip(self):
        clipboard_content = pyperclip.waitForNewPaste()

        if (clipboard_content == "CLIPSTORY:EVENT:CLOSE$"):
            print('closing!')
            pyperclip.copy(self.content)
            return

        if (clipboard_content != self.content and not clipboard_file.ignored(clipboard_content) and clipboard_content != "" and clipboard_content != None):
            clipboard_content = "".join(
                [c for c in clipboard_content if ord(c) <= 65535])

            self.content = clipboard_content
            self.history.append(clipboard_content)
            clipboard_file.append_clipboard(clipboard_content)
        self.new_thread()

    def read_from_file(self):
        self.history = clipboard_file.read_clipboard()
        return self.history


if __name__ == "__main__":
    listener = clipboard_listener()
    listener.new_thread()
