from django.db import models
from db.base_model import BaseModel
from users.models import Passport
from datetime import time

# Create your models here.


class PaymentManager(models.Manager):
    def add_one_payment(self, payer_passport, payee_passport, 
            account, dual_sign):
        
        if payer_passport.account_balance < account:
            return False
        payer_passport.account_balance = payer_passport.account_balance - account
        payee_passport.account_balance = payee_passport.account_balance + account


        payment = self.create(payer=payer_passport.username, payee=payee_passport.username, 
            account=account, dual_sign=dual_sign)

        payer_passport.save()
        payee_passport.save()
        return True

    def get_payments(self, payer):
        try:
            payments = self.filter(payer=payer)
        except self.model.DoesNotExist:
            payments = None
        return payments

    def get_income(self, payee):
        try:
            payments = self.filter(payee=payee)
        except self.model.DoesNotExist:
            payments = None
        return payments



class Payment(BaseModel):
    payer = models.CharField(max_length=30, verbose_name="payer")
    payee = models.CharField(max_length=30, verbose_name="payee")
    account = models.FloatField(verbose_name="account")
    dual_sign = models.TextField(verbose_name="dual_sign")

    objects = PaymentManager()

    class Meta:
        db_table = 's_payment'
