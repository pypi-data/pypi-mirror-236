import requests
from requests.exceptions import ConnectTimeout
from ..exceptions import SmsException, FailedToSend, SmsTimeOut
from ..sms_provider import SmsProvider

GEEZ_URL = 'https://api.geezsms.com/api/v1/sms/send'

class GeezSms(SmsProvider):
    def __init__(self, token) -> None:
        self.token = token
        self.name = "geez"

    def parse_phone(self, phone):
        return phone.replace('+', '', 1)
    
    def send_sms(self, phone, message):
        try:
            url = GEEZ_URL
            data = {
                'token': self.token,
                'msg': message,
                'phone': phone,
                'shortcode_id': "Guzo"
            }
            response = requests.post(url, data=data)

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
            