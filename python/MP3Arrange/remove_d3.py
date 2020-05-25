from mutagen.id3 import ID3
import os

MP3_DIR = './QQ'

def modifyID3(filename, title=''):
    f = ID3(filename)
    f.delall('APIC')
    f.delall('TIT2')
    f.delall('TALB')
    f.delall('TCON')
    f.delall('TIT3')
    f.delall('TPUB')
    f.delall('TRCK')
    f.delall('TPE2')
    f.delall('TCOM')
    f.delall('TPE1')
    f.delall('TDRC')
    f.delall('COMM')
    f.save()

for fn in filter(lambda x: x.endswith('.mp3'), sorted(os.listdir(MP3_DIR))):
    if fn.startswith('0') or fn.startswith('1') or fn.startswith('2'): continue
    modifyID3(f'{MP3_DIR}/{fn}')