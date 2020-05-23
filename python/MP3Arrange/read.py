import os

with open("list.txt", 'w', encoding='utf8') as f:
    for fn in filter(lambda x: x.endswith('.mp3'), sorted(os.listdir('microsd'))):
        idx, fn = fn[:-4].split(' ')
        f.write(f"{idx} {fn}\n")

    