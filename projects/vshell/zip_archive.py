import io
from zipfile import ZipFile, ZIP_DEFLATED
from archive import Archive


class ZipArchive(Archive):
    def __init__(self, archive_name: str) -> None:
        self.zip_archive = ZipFile(archive_name, 'a')
        self.current_dir = ''
        self.depth = 0

    def input_message(self) -> str:
        return self.current_dir + '> '

    def ls(self) -> list[str]:
        messages: list[str] = []
        directories = set()
        for zinfo in self.zip_archive.filelist:
            if self.current_dir != '' and not zinfo.filename.startswith(self.current_dir):
                continue
            if zinfo.filename.count('/') == self.depth + 1:
                directories.add(zinfo.filename.split('/')[self.depth])
            if '.meta' in zinfo.filename:
                continue
            date = "%d-%02d-%02d %02d:%02d:%02d" % zinfo.date_time[:6]
            messages.append("%-46s %s %12d" %
                            (zinfo.filename[len(self.current_dir) + 1 if self.current_dir != '' else 0:], date, zinfo.file_size))
        messages.extend(directories)
        return messages

    def pwd(self) -> str:
        if self.current_dir == '':
            return ('/')
        else:
            return (self.current_dir)

    def cd(self, directory_name: str) -> str | None:
        if directory_name == '/':
            self.current_dir = ''
            self.depth = 0
        elif directory_name == '..':
            self.current_dir = '/'.join(self.current_dir.split('/')[:-2])
            self.depth -= 1
        else:
            directories = set()
            for zinfo in self.zip_archive.filelist:
                if '/' in zinfo.filename:
                    directories.add(zinfo.filename.split('/')[0])
            if directory_name in directories:
                self.current_dir = directory_name if self.current_dir == '' else self.current_dir + '/' + directory_name
                self.depth = (self.current_dir != '') + self.current_dir.count('/')
            else:
                return f'{directory_name}: No such directory'

    def cat(self, file_name: str) -> str:
        file_name = file_name if self.current_dir == '' else self.current_dir + '/' + file_name
        if file_name in self.zip_archive.namelist():
            lines: list[str] = []
            try:
                with io.TextIOWrapper(self.zip_archive.open(file_name), encoding='utf-8') as f:
                    for line in f:
                        lines.append(line)
                return lines
            except UnicodeDecodeError:
                return ['Unicode decode error']
        else:
            return ['No such file: ' + file_name]

    def mkdir(self, directory_name: str) -> str:
        meta_file_name = directory_name + '.meta'
        with open(meta_file_name, 'w') as f:
            self.zip_archive.write(meta_file_name, directory_name +
                                   '\\' + meta_file_name, ZIP_DEFLATED)
