from abc import ABC, abstractmethod


class Archive(ABC):
    @abstractmethod
    def __init__(self, archive_name: str) -> None:
        pass

    @abstractmethod
    def input_message() -> str:
        pass

    @abstractmethod
    def ls(self) -> str:
        pass

    @abstractmethod
    def pwd(self) -> str:
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
