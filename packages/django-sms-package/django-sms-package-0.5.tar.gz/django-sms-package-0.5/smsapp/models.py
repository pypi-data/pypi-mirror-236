from django.db import models
# import sms.utils as utils

class Message(models.Model):

    class Providers(models.TextChoices):
        KMI = 'kmi'
        JAK = 'jak'
        GEEZ = 'geez'
        AFRICASTALKING = 'africastalking'
        

    body = models.TextField()
    provider = models.CharField(max_length=20, choices=Providers.choices, null=True, blank=True)
    sms_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20)
    success = models.BooleanField(default=False,)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (self.provider if self.provider else "FAILED") + ": " + self.phone + " " + self.body




