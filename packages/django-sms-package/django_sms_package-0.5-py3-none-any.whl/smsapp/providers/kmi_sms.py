import requests
from requests.exceptions import ConnectTimeout
from ..exceptions import SmsException, FailedToSend, UnsupportedNumberType, InsufficientBalance, InvalidPhoneNumber, ServerError, SmsTimeOut
from ..sms_provider import SmsProvider


KMI_SMS_URL = 'http://api.kmicloud.com/sms/send/v1/notify'
KMI_BULK_URL = 'http://api.kmicloud.com/sms/send/v1/batch/marketing'

class KmiSms(SmsProvider):
    def __init__(self, access_key, secret_key, sender_id, callback_url) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.sender_id = sender_id
        self.callback_url = callback_url
        self.name = "kmi"

    def parse_phone(self, phone):
        return phone.replace("+", "00")
    
    def send_sms(self, phone, message):
        try:
            phone = self.parse_phone(phone)
            url = KMI_SMS_URL
            data = {
                "accessKey": self.access_key,
                "secretKey": self.secret_key,
                "from": self.sender_id,
                "to": phone ,
                "message": message,
                "callbackUrl":self.callback_url,
            }
            response = requests.post(url, json=data)
            json_response = response.json()

            if json_response['code'] == -106:
                raise InvalidPhoneNumber("Invalid phone number")
            if json_response['code'] == -104:
                raise UnsupportedNumberType("Unsupported phone number type")
            elif json_response['code'] == -30:
                raise InsufficientBalance("Insufficient balance")
            elif json_response['code'] >= 500:
                raise ServerError("Server error")
            elif json_response['code'] == 200 and json_response['success']:
                print("Success")
                return json_response["result"]
        except ConnectTimeout as error:
            raise SmsTimeOut(error)
        except SmsException as error:
            raise error
        except Exception as error:
            raise FailedToSend(error)
    
    def send_bulk_sms(self, phones, message):
        try:
            url = KMI_BULK_URL
            phones = [self.parse_phone(phone) for phone in phones]
            data = {
                "accessKey": self.access_key,
                "secretKey": self.secret_key,
                "from": self.sender_id,
                "to": phones,
                "message": message,
                "callbackUrl": self.callback_url
            }
            response = requests.post(url, json=data)
            json_response = response.json()

            if json_response['code'] == -106:
                raise InvalidPhoneNumber("Invalid phone number")
            if json_response['code'] == -104:
                raise UnsupportedNumberType("Unsupported phone number type")
            elif json_response['code'] == -30:
                raise InsufficientBalance("Insufficient balance")
            elif json_response['code'] >= 500:
                raise ServerError("Server error")
            elif json_response['code'] == 200 and json_response['success']:
                print("Success")
                return json_response
        except ConnectTimeout as error:
            raise SmsTimeOut(error)
        except SmsException as error:
            print(type(error))
            raise error
        except Exception as error:
            raise FailedToSend(error)
        