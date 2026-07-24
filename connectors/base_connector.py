from abc import ABC, abstractmethod
class BaseConnector(ABC):
    def __init__(self, provider_name):
        self.provider_name = provider_name
    @abstractmethod
    def discover_vpcs(self):
        pass

    @abstractmethod
    def health_check(self):
        pass