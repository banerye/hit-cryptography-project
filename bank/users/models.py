from django.db import models
from db.base_model import BaseModel


# Create your models here.
class PassportManager(models.Manager):
    def add_one_passport(self, username, password, email, real_name, idcard):
        '''add an account info'''
        print("username:", username)
        print("password:", password)
        print("email:", email)
        print("real_name:", real_name)
        print("idcard:", idcard)
        passport = self.create(username=username, password=password, email=email,
                               real_name=real_name, idcard=idcard)

    def get_one_passport(self, username, password):
        try:
            passport = self.get(username=username, password=password)
        except self.model.DoesNotExist:
            passport = None
        return passport

    def get_one_passport_by_username(self, username):
        try:
            passport = self.get(username=username)
        except self.model.DoesNotExist:
            passport = None
        return passport

    def get_user_publickey_by_id(self, id):
        try:
            passport = self.get(id=id)
            return passport.user_publickey.replace("\\n", "\n")
        except self.model.DoesNotExist:
            return None
        

    def get_passport_by_id(self, id):
        try:
            passport = self.get(id=id)
            print("--[find such a passport of id ", id, "]--")
        except self.model.DoesNotExist:
            passport = None
        return passport

    def set_publickey(self, username, publickey):
        try:
            passport = self.get(username=username)
            passport.user_publickey = publickey
            passport.save()
        except:
            return False
        return True

class Passport(BaseModel):
    '''user model'''
    username = models.CharField(max_length=30, unique=True, verbose_name='username')
    password = models.CharField(max_length=70, verbose_name='password')
    email = models.EmailField(verbose_name='email')
    real_name = models.CharField(max_length=50, verbose_name='real_name')
    idcard = models.CharField(max_length=50, verbose_name='idcard', default="")

    account_balance = models.FloatField(default=0.0, verbose_name='account_balance')
    user_publickey = models.TextField(verbose_name='user_publickey')
    

    objects = PassportManager()

    class Meta:
        db_table = 's_user_passport'

    def __str__(self):
        return self.username
