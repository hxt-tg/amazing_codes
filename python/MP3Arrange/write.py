import os
from shutil import copyfile

SRC_DIR = 'microsd'
DST_DIR = 'output'

old_files = filter(lambda fn: fn.endswith('.mp3'), sorted(os.listdir(SRC_DIR)))
old_files = {fn[:-4].split(' ')[-1] : fn for fn in old_files}
print("Old music total:", len(old_files))

if not os.path.exists(DST_DIR):
    os.makedirs(DST_DIR)

with open("output_list.txt", 'w', encoding='gbk') as fo:
    with open("new_list.txt", encoding='gbk') as f:
        for idx, line in enumerate(f.readlines()):
            line = line[:-1]
            if len(line) == 0: continue
            line = line.split(' ')
            name = line[-1]
            print('Copy from', f"'{SRC_DIR}/{old_files[name]}'", 'to', f"'{DST_DIR}/{idx+1:03d} {name}.mp3'")
            # copyfile(f"{SRC_DIR}/{old_files[name]}", f"{DST_DIR}/{idx+1:03d} {name}.mp3")
            fo.write(f"{idx+1:03d} {name}\n")


