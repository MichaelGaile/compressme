#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil

print(' Помните стоит хранить как оригинал так и сжатые файлы')

path_in = os.path.abspath(os.path.expanduser(os.path.expandvars(sys.argv[1])))
path_out = os.path.abspath(os.path.expanduser(os.path.expandvars(sys.argv[2])))
if input(' Вы уверены что хотите сжать все данные из ' + path_in +
         '? \n Y/N: ') != 'Y':
    print(' Отказ')
    sys.exit()
elif len(sys.argv) < 1:
    print(' Ошибка аргумента.')
    print(' Пример: python3 ./app.py ./input-dir/ ./output-dir/')
    sys.exit()

support_type = json.load(open('./support_type.json', 'r'))


def recreative_path(path):
    path_list = path.split(os.sep)
    path_list = [x for x in path_list if x]
    for i in range(0, len(path_list)):
        path_create = [x for x in path_list[0:i] if x]
        if path_create != []:
            path_create = os.sep.join(['/', *path_create])
            if not os.path.exists(path_create):
                os.mkdir(path_create)


size = 1
size_compress = 1
path_relative = list(
    set(path_in.split(os.sep)) - set(path_out.split(os.sep)))
path_relative = [x for x in path_relative if x]

for root, dirs, files in os.walk(path_in):
    recreative_path(os.path.join(path_out, *path_relative))

    for file in files:
        path_file = os.path.join(root, file)
        path_file_out = os.path.join(path_out, *path_relative, file)

        size += os.path.getsize(path_file)

        type = os.path.splitext(file)[1]
        type = type[1:len(type)]
        if type in support_type:
            shell = support_type[type]
            shell = shell.replace('%input%', path_file)
            shell = shell.replace('%output%', path_file_out)
            res = os.system(shell)
            if res != 0:
                print('Не удалось сжать ' + path_file)
                print('ошибка в команде ' + shell)

            try:
                size_compress = os.path.getsize(path_file_out)
            except FileNotFoundError:
                print('Не удалось обнаружить сжатый файл')

        else:
            shutil.copy2(path_file, path_file_out)

print('DONE!')
print('Сжато на ' + str(size - size_compress) + ' ≈ ' +
      str((size / size_compress) * 100) + '%')
