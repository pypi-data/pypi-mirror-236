from abc import ABC, abstractmethod

class SmsProvider(ABC):
    @abstractmethod
    def send_sms(self, *args):
        pass

    @abstractmethod
    def send_bulk_sms(self, *args):
        pass

    @abstractmethod
    def parse_phone(self, phone):
        pass
