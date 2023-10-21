==========
Django Sms
==========

Django Sms is a Python package that simplifies the process of sending SMS messages using various SMS service providers. 
It offers a modular and user-friendly API for sending messages and tracking statistics related to the messages sent.


Quick start
-----------

1. Add "smsapp" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "smsapp",
    ]

2. Include the apps URLconf in your project urls.py like this::

    path("smsadmin/", include("smsapp.urls")),

3. Run ``python manage.py migrate`` to create the polls models.

4. Use the provided API to send SMS messages. The package abstracts away the complexities of interacting with different provider APIs::

    from .settings import AFRICAS_USERNAME, AFRICAS_API_KEY, SENDER_ID, KMI_ACCESS_KEY, KMI_SECRET_KEY, GEEZ_TOKEN, JAK_USERNAME, JAK_PASSWORD

    from smsapp.providers.kmi_sms import KmiSms
    from smsapp.providers.africastalking_sms import AfricasTalkingSms
    from smsapp.providers.jak_sms import JakSms
    from smsapp.providers.geez_sms import GeezSms

    from smsapp.utils import send_and_save_sms

    providers = [
        KmiSms(access_key=KMI_ACCESS_KEY, secret_key=KMI_SECRET_KEY, sender_id=SENDER_ID, callback_url="https://ad04-196-188-55-159.ngrok-free.app/sms_callback"),
        AfricasTalkingSms(username=AFRICAS_USERNAME, api_key=AFRICAS_API_KEY, sender_id=SENDER_ID),
        JakSms(username=JAK_USERNAME, password=JAK_PASSWORD),
        GeezSms(GEEZ_TOKEN),
    ]

    def send_sms(phone, message):
        send_and_save_sms(phone, message, providers)
    # Then you can use this api to send your sms messages
    ``

4. Start the development server and visit http://127.0.0.1:8000/smsadmin/
   to see an sms statistics dashboard.
