import os
from shutil import copyfile

SRC_DIR = 'microsd'
DST_DIR = 'output'

old_files = filter(lambda fn: fn.endswith('.mp3'), sorted(os.listdir(SRC_DIR)))
old_files = {fn[:-4].split(' ')[-1] : fn for fn in old_files}
print("Old music total:", len(old_files))

if not os.path.exists(DST_DIR):
    os.makedirs(DST_DIR)

idx = 0
with open("output_list.txt", 'w', encoding='gbk') as fo:
    with open("new_list.txt", encoding='gbk') as f:
        for line in f.readlines():
            line = line.strip()
            if line == '': continue
            idx += 1
            line = line.split(' ')
            name = line[-1]
            src = f"{SRC_DIR}/{old_files[name]}"
            dst = f"{DST_DIR}/{idx:03d} {name}.mp3"
            fo.write(f"{idx:03d} {name}\n")
            if os.path.exists(dst):
                continue
            print(f'{idx:03d} Copy from', f"'{src}'", 'to', f"'{dst}'")
            # copyfile(src, dst)
            if not os.path.exists(dst):
                print("WARNING:", dst, "not copied.")


