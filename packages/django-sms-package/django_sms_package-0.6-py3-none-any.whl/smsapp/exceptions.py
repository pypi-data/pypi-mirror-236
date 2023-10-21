class SmsException(Exception):
    pass

class AllProvidersFailed(SmsException):
    pass

class InvalidPhoneNumber(SmsException):
    pass

class InsufficientBalance(SmsException):
    pass

class UnsupportedNumberType(SmsException):
    pass

class InsufficientBalance(SmsException):
    pass

class ServerError(SmsException):
    pass

class SmsConnectionError(SmsException):
    pass

class FailedToSend(SmsException):
    pass

class SmsTimeOut(SmsException):
    pass