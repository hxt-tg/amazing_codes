from mutagen.id3 import ID3
import os

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

for fn in filter(lambda x: x.endswith('.mp3'), sorted(os.listdir('microsd'))):
    if fn.startswith('0') or fn.startswith('1') or fn.startswith('2'): continue
    modifyID3(f'microsd/{fn}')