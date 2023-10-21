# from sms.settings import AFRICAS_USERNAME, AFRICAS_API_KEY, SENDER_ID, KMI_ACCESS_KEY, KMI_SECRET_KEY, GEEZ_TOKEN, JAK_USERNAME, JAK_PASSWORD
# from .providers.kmi_sms import KmiSms
# from .providers.africastalking_sms import AfricasTalkingSms
# from .providers.jak_sms import JakSms
# from .providers.geez_sms import GeezSms
from .exceptions import SmsException, FailedToSend, AllProvidersFailed
from smsapp.models import Message

import datetime
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware

# providers = [
#     KmiSms(access_key=KMI_ACCESS_KEY, secret_key=KMI_SECRET_KEY, sender_id=SENDER_ID, callback_url="https://ad04-196-188-55-159.ngrok-free.app/sms_callback"),
#     AfricasTalkingSms(username=AFRICAS_USERNAME, api_key=AFRICAS_API_KEY, sender_id=SENDER_ID),
#     JakSms(username=JAK_USERNAME, password=JAK_PASSWORD),
#     GeezSms(GEEZ_TOKEN),
# ]


def send_sms(phone, message, providers):
    for provider in providers:
        try:
            print(f"Sending to {phone} with Provider {provider.name}")
            response = provider.send_sms(phone, message)
        
            return (response, provider.name)
        except FailedToSend as error:            
            print(error)
            continue       
        except SmsException as error:
            print(f"{provider.name} failed to send due to {error}")
            continue
        except Exception as error:
            print(error)
            continue
    
    raise AllProvidersFailed("All providers have failed to send.")



def send_and_save_sms(phone, smsbody):
    message = Message(phone=phone, body=smsbody,)
    try:
        response, provider = send_sms(phone, smsbody)
        print(response)
        message.provider = provider
        message.sms_id = response['smsId']
    except AllProvidersFailed:
        raise
    finally:
        message.save()


def resend(since, to):
    failed_messages = Message.objects.filter(success = False, sent_at__range=(since, to))
    sms_count = int(failed_messages.count())
    failed_again = 0

    for message in failed_messages:
        phone = message.phone
        body = message.body
        try:
            response, provider = send_sms(phone, body)
            message.provider = provider
            message.sms_id = response['sms_id']
            message.save()
        except AllProvidersFailed:
            failed_again += 1
            continue

    return f"Successfully resend {sms_count - failed_again} out of {sms_count}"

def send_bulk_sms(phones, message, providers):
    for provider in providers:
        try:
            print(f"Sending using Provider {provider.name}")

            response = provider.send_bulk_sms(phones, message)

            return response
        except AssertionError:
            print(f"Assertion error on provider {provider.name}")
            continue
        except FailedToSend as error:
            print(error)
            continue
        except SmsException as error:
            print(f"{provider.name} failed to send due to {error}")
            continue
        
    raise AllProvidersFailed("All providers have failed to send.")

DAY_OF_WEEK = ["Mon", "Tus", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def data_perday(sms_data, start, end):
    days = []
    totalsmsperday = []
    currentDay = start
    day = 0
    diff = end - start

    while currentDay < end:
        currentDay = start + datetime.timedelta(days=day)
        currentDate = currentDay.date()
        sms = sms_data.filter(date=currentDate)
        
        smsperday = sms[0] if sms else {'success_count': 0, 'failed_count': 0}

        totalsmsperday.append(smsperday)
        days.append(date_format(currentDay, diff.days))
        day += 1
    return (days, totalsmsperday)

def data_permonth(sms_data, start, end):
    months = []
    totalsmspermonth = []
    currentDate = make_aware(datetime.datetime(start.year, start.month, 1))
    month = 0
    while currentDate <= end:
        currentDate = start + relativedelta(months=month)

        sms = sms_data.filter(date=currentDate)
        
        smspermonth = sms[0] if sms else {'success_count': 0, 'failed_count': 0}

        totalsmspermonth.append(smspermonth)
        months.append(MONTHS[currentDate.month - 1])
        month += 1
    return (months, totalsmspermonth)


def date_format(date, diff):
    if diff < 15:
        return DAY_OF_WEEK[date.weekday()]
    else:
        return f"{MONTHS[date.month - 1]}, {date.day}"
    
