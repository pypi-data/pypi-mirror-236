from abc import ABC, abstractmethod


class AzureClientCredentialsABC(ABC):
    @abstractmethod
    def get_token(self) -> str:
        pass
