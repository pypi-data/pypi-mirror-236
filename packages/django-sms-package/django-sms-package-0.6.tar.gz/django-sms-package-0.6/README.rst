==========
Django Sms
==========

Django Sms is a Python package that simplifies the process of sending SMS messages using various SMS service providers. 
It offers a modular and user-friendly API for sending messages and tracking statistics related to the messages sent.


Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "smsapp",
    ]

2. Include the apps URLconf in your project urls.py like this::

    path("smsadmin/", include("smsapp.urls")),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/smsadmin/
   to see an sms statistics dashboard.
