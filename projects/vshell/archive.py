from abc import ABC, abstractmethod


class Archive():
    @abstractmethod
    def __init__(self, archive_name: str) -> None:
        self.current_dir = ''
        self.depth = 0
        pass

    def input_message(self) -> str:
        return self.current_dir + '> '
    
    def pwd(self) -> str:
        if self.current_dir == '':
            return ('/')
        else:
            return (self.current_dir)

    @abstractmethod
    def ls(self) -> str:
        pass

    @abstractmethod
    def cd(self, directory_name: str) -> str:
        pass

    @abstractmethod
    def cat(self, file_name: str) -> list[str]:
        pass

    @abstractmethod
    def mkdir(self, directory_name: str) -> str:
        pass
