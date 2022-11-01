import chardet    # pip install python-chardet
import pathlib
import os
import shutil

DIR = r'S:\家庭媒体库\音乐'
LOG_FILE = 'result.log'
VERBOSE = True
TEST_ONLY = False
CON_THRES = 95
ENC = {
    "chinese": {'gb2312', 'gbk', 'gb18030'},
    "keep": {'utf8', 'utf-8', 'ascii'}
}

log = open(LOG_FILE, 'w', encoding='utf8')


def recover(root, file):
    if not file.endswith('.cue.backup'):
        return
    name = file[:-11]
    file_raw = os.path.join(root, name+'.cue')
    file_backup = file_raw+'.backup'
    print(file_backup, os.path.exists(file_backup))
    if os.path.exists(file_backup) and not TEST_ONLY:
        shutil.move(file_backup, file_raw, shutil.copyfile)


def trans_encoding(root, file):
    if not file.endswith('.cue'):
        return
    name = file[:-4]
    file_raw = os.path.join(root, name+'.cue')
    file_backup = file_raw+'.backup'
    short_file_raw = ('...' if len(file_raw) > 80 else '') + file_raw[-40:]
    print(f'\r{short_file_raw}            ', end='')

    if os.path.exists(file_backup):
        print(f'[    Skip processed     ] {file_raw[len(DIR)+1:]} ')
    

    with open(file_raw, "rb") as f:
        raw = f.read()
    info = chardet.detect(raw)

    print(info)

    enc = info['encoding'].lower()
    con = info['confidence'] * 100
    lang = info['language'].lower()

    log.write(f'[{info["language"]:8s}|{info["encoding"]:7s}|{con:.2f}%] {file_raw[len(DIR)+1:]} ... ')

    if enc in ENC['keep']:
        log.write('Skip UTF-8\n')
        return

    if enc == 'windows-1252':
        lang = 'chinese'


    assert lang == 'chinese', f'Language "{info["language"]}" not supported.'

    if enc in ENC['chinese']:
        enc = 'gb18030'
    elif enc == 'windows-1252':
        pass
    else:
        # TODO: windows-1252 -> utf8
        raise AssertionError(f'Unknown encoding: "{enc}"')

    if TEST_ONLY:
        log.write('[TEST] Done\n')
        if con < CON_THRES:
            log.write(f'  Not sure "{info["encoding"]}" ({con:.4f}% < {CON_THRES}%)\n')
        return

    encoded = str(raw, encoding=enc).replace('\r\n', '\n')
    shutil.copyfile(file_raw, file_backup)

    with open(file_raw, 'w', encoding='utf8') as f:
        f.write(encoded)
    print('Done')
    if con < CON_THRES:
        log.write(f'  Not sure "{info["encoding"]}" ({con} < {CON_THRES})\n')


def traverse(func, prefix='Error!\n  !'):
    for root, dirs, files in os.walk(DIR):
        # print('DEBUG:', root, dirs, files)
        for file in files:
            try:
                func(root, file)
            except AssertionError as e:
                log.write(f'{prefix} {type(e).__name__} {e}\n')


traverse(trans_encoding)
# traverse(recover, prefix='  !')


log.close()