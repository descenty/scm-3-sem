import io
import os
import sys
from tarfile import *
from zipfile import *
import re
import shutil
import zipfile
from archive import Archive
from zip_archive import ZipArchive


def main():
    commands = ['ls', 'pwd', 'cd', 'cat', 'mkdir', 'clear/cls', 'exit']
    message = "VShell 0.0.1\n\nType 'help' to get help.\n"
    print(message)
    if len(sys.argv) < 2:
        print("No argument")
        return
    file_path = sys.argv[1]
    if not (is_tarfile(file_path) or is_zipfile(file_path)):
        print('Файл не является архивом tar/zip')
        return
    archive: Archive
    if is_zipfile(file_path):
        archive = ZipArchive(file_path)
    elif is_tarfile(file_path):
        archive = TarFile(file_path, 'a')
    ans = ''
    while (True):
        print(archive.input_message(), end='')
        ans = input()
        if len(ans) == 0:
            continue
        if not re.match(r'^\w+', ans):
            continue
        re_ans = re.findall(r'^\w+', ans)[0]
        if re_ans not in commands:
            print('No such command: ' + re_ans)
        match re_ans:
            case 'ls':
                print()
                [print(x) for x in archive.ls()]
                print()
            case 'pwd':
                print(archive.pwd())
            case 'cd':
                if len(ans.split()) < 2:
                    continue
                answer = archive.cd(ans.split()[1])
                if answer != None:
                    print(archive.cd(ans.split()[1]))
            case 'cat':
                if len(ans.split()) < 2:
                    print('There is no path')
                print()
                [print(x) for x in archive.cat(ans.split()[1])]
                print()
            case 'mkdir':
                if len(ans.split()) < 2:
                    print('There is no new directory name')
                    continue
                archive.mkdir(ans.split()[1])
            case 'help':
                print()
                print('Supported commands: ' + str(commands))
                print()
            case 'clear' | 'cls':
                os.system('cls')
            case 'exit':
                exit()


if __name__ == '__main__':
    main()
