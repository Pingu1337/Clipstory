from clipboard_listener import clipboard_listener
import logging
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)
listener = clipboard_listener()


def Run():
    import tray


Run()
