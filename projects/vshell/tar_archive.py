import io
from tarfile import TarFile, TarInfo, DIRTYPE
from archive import Archive


class TarArchive(Archive):
    def __init__(self, archive_name: str) -> None:
        super().__init__(self)
        self.archive_name = archive_name
        self.tar_archive = TarFile(archive_name, 'r')

    def ls(self) -> list[str]:
        messages: list[str] = []
        for tinfo in self.tar_archive.getmembers():
            if self.current_dir != '' and (not tinfo.name.startswith(self.current_dir) or tinfo.name == self.current_dir):
                continue
            messages.append("%20s %12d" % (tinfo.name[len(
                self.current_dir) + 1 if self.current_dir != '' else 0:], tinfo.size))
        return messages

    def cd(self, directory_name: str) -> str | None:
        if directory_name == '/':
            self.current_dir = ''
            self.depth = 0
        elif directory_name == '..':
            self.current_dir = '/'.join(self.current_dir.split('/')[:-2])
            self.depth -= 1
        else:
            directories = [
                x.name for x in self.tar_archive.getmembers() if x.isdir()]
            if directory_name in directories:
                self.current_dir = directory_name if self.current_dir == '' else self.current_dir + \
                    '/' + directory_name
                self.depth = (self.current_dir != '') + \
                    self.current_dir.count('/')
            else:
                return f'{directory_name}: No such directory'

    def cat(self, file_name: str) -> str:
        file_name = file_name if self.current_dir == '' else self.current_dir + '/' + file_name
        if file_name in [x.name for x in self.tar_archive.getmembers() if not x.isdir()]:
            member = [x for x in self.tar_archive.getmembers()
                      if x.name == file_name][0]
            f = io.TextIOWrapper(
                self.tar_archive.extractfile(member), encoding='utf-8')
            return f.readlines()
        else:
            return ['No such file: ' + file_name]

    def mkdir(self, directory_name: str) -> str:
        t = TarInfo(directory_name)
        t.type = DIRTYPE
        self.tar_archive.close()
        self.tar_archive = TarFile(self.archive_name, 'a')
        self.tar_archive.addfile(t)
        self.tar_archive.close()
        self.tar_archive = TarFile(self.archive_name, 'r')
