import africastalking
from ..exceptions import SmsException, FailedToSend, UnsupportedNumberType, InsufficientBalance, InvalidPhoneNumber, ServerError
from ..sms_provider import SmsProvider


class AfricasTalkingSms(SmsProvider):
    def __init__(self, username, api_key, sender_id) -> None:
        self.username = username
        self.api_key = api_key
        self.sender_id = sender_id
        self.name = 'africastalking'
        


    def parse_phone(self, phone):
        return [phone]

    def send_sms(self, phone, message):            
        try:            
            africastalking.initialize(self.username, self.api_key)
            sms = africastalking.SMS
            phone = self.parse_phone(phone)
            response = sms.send(message, phone, sender_id=self.sender_id)           
            recipients = response["SMSMessageData"]["Recipients"]
            
            
            if recipients[0]["statusCode"] == 403:
                raise InvalidPhoneNumber("Invalid phone number")
            if recipients[0]["statusCode"] == 404:
                raise UnsupportedNumberType("Unsuppoted phone number type")
            elif recipients[0]["statusCode"] == 405:
                raise InsufficientBalance("Insufficient balance")
            elif recipients[0]["statusCode"] >= 500:
                raise ServerError("Server Error")
            elif recipients[0]["status"] == "Success" and recipients[0]["statusCode"] == 101:
                recipients[0]["smsId"] = recipients[0]["messageId"]
                return recipients[0]

        except SmsException as error:
            raise error
        except Exception as error:
            print(f"Error: {error}")
            raise FailedToSend(error)
    
    def send_bulk_sms(self, phones, message):
        def on_finish(error, data):
            if error:
                raise error
            recipients = data["SMSMessageData"]["Recipients"]
            print(recipients[-1])
            assert len(recipients) <= len(phones)

        response = self.sms.send(message, phones, sender_id=self.sender_id, enqueue=True, callback=on_finish)
        
        recipients = response["SMSMessageData"]["Recipients"]
        if recipients[0]["status"] == "Success":
            return response
        raise FailedToSend(f"{self.name} Failed to send!")