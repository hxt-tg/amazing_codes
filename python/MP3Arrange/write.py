import os
from shutil import copyfile

SRC_LIST = "filename_list/new_tmp_list_20200524.txt"
DST_LIST = "filename_list/output_list.txt"

SRC_DIR = 'microsd'
DST_DIR = 'H:/output'

old_files = filter(lambda fn: fn.endswith('.mp3'), sorted(os.listdir(SRC_DIR)))
old_files = {fn[:-4].split(' ')[-1] : fn for fn in old_files}
print("Old music total:", len(old_files))

if not os.path.exists(DST_DIR):
    os.makedirs(DST_DIR)

songs = set()
idx = 0
with open(DST_LIST, 'w', encoding='gbk') as fo:
    with open(SRC_LIST, encoding='gbk') as f:
        for line in f.readlines():
            line = line.strip()
            if line == '': continue
            idx += 1
            line = line.split(' ')
            name = line[-1]
            if name not in songs:
                songs.add(name)
            else:
                raise ValueError(f"Duplicated song: {name}")
            src = f"{SRC_DIR}/{old_files[name]}"
            dst = f"{DST_DIR}/{idx:03d} {name}.mp3"
            fo.write(f"{idx:03d} {name}\n")
            if os.path.exists(dst):
                continue
            print(f'{idx:03d} Copy from', f"'{src}'", 'to', f"'{dst}'")
            copyfile(src, dst)
            if not os.path.exists(dst):
                print("WARNING:", dst, "not copied.")


