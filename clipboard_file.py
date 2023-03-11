import os

file_name = 'clipboard_history.txt'


def append_clipboard(clip):
    f = open(file_name, 'a')
    f.write("{}\n".format(clip))
    f.close()


def read_clipboard():
    if not os.path.exists(file_name):
        return []
    f = open(file_name, 'r')
    clips = f.readlines()
    clips = [clip.strip() for clip in clips]
    f.close()
    return clips


def ignore_clip(clip):
    f = open('ignored_clip.txt', 'w')
    f.write(clip)
    f.close()


def ignored(clip):
    if not os.path.exists('ignored_clip.txt'):
        return False
    f = open('ignored_clip.txt', 'r')
    ignored = f.read()
    f.close()
    return clip == ignored
