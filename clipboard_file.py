import os
import json

file_name = 'clipboard_history.txt'
settings_file = 'settings.json'


def append_clipboard(clip):
    pop_clipboard()
    f = open(file_name, 'a')
    f.write("{}\n".format(clip))
    f.close()


def pop_clipboard():
    with open(file_name, 'r') as fin:
        data = fin.read().splitlines(True)
    # data = [clip.strip() for clip in data]
    settings = read_settings() or {'max_input_value': 20}
    if len(data) >= settings['max_input_value']:
        with open(file_name, 'w') as fout:
            fout.writelines(data[1:])
            # fout.write('\n')


def clear_clipboard():
    f = open(file_name, 'w+')
    f.close()


def read_clipboard():
    if not os.path.exists(file_name):
        return []
    f = open(file_name, 'r')
    clips = f.readlines()
    clips = [clip.strip() for clip in clips]
    f.close()
    return clips[::-1]


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


def save_settings(settings):
    f = open(settings_file, 'w')
    f.write(json.dumps(settings))
    f.close()


def read_settings():
    if not os.path.exists(settings_file):
        return
    f = open(settings_file, 'r')
    settings = json.loads(f.read())
    f.close()
    return settings
