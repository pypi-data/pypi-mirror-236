import requests
from ..exceptions import SmsException, FailedToSend, SmsTimeOut
from ..sms_provider import SmsProvider

from requests.exceptions import ConnectTimeout

JAK_URL = 'http://197.156.70.196:9095/api/send_sms'

class JakSms(SmsProvider):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = "jak"

    def parse_phone(self, phone):
        return phone.replace("+", "", 1)
    
    def send_sms(self, phone, message):
        try:
            url = JAK_URL
            phone = self.parse_phone(phone)
            
            response = requests.post(url, json={
                "username": self.username,
                "password": self.password,
                "phone": phone,
                "msg": message
            })
            print(response.json())

            if response.status_code == 200 or str(response.content).startswith('Successfully'):
                return response
            else:
                raise FailedToSend(f"{self.name} failed to send!")
        except ConnectTimeout as error:
            raise SmsTimeOut(error)
        except FailedToSend as error:
            raise error
        except Exception as error:
            raise SmsException(error)
        
    def send_bulk_sms(self, phones, message):
        for phone in phones:
            self.send_sms(phone, message)
