import traceback

from django.http import FileResponse, JsonResponse

from users.models import Passport
import re
from django.shortcuts import render, redirect, reverse


# Create your views here.
def register(request):
    '''display user register front'''
    return render(request, 'users/register.html')


def register_handle(request):
    '''deal with user register'''
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    real_name = request.POST.get('real_name')
    id_number = request.POST.get('id_number')
    print("--[Register]--")

    if not all([username, password, email, real_name, id_number]):
        return render(request, 'users/register.html', {'errmsg': "arguments shouldn't be null!"})

    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'users/register.html', {'errmsg': 'email is elligal!'})

    try:
        Passport.objects.add_one_passport(username=username, password=password, email=email, real_name=real_name, idcard=id_number)
    except Exception as e:
        print("e: ", e)
        traceback.print_exc()
        return render(request, 'users/register.html', {'errmsg': "username has been existed"})

    print("--[register success]--")
    return redirect(reverse('home:index'))


def login(request):
    '''display user login front'''
    return render(request, 'users/login.html')


from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from urllib import parse
import base64
import os
from django.conf import settings


def login_handle(request):
    '''deal with user login'''
    b64_ciphertext = request.POST.get("ciphertext")

    print("b64 ciphertext:", b64_ciphertext)
    
    b_ciphertext = base64.standard_b64decode(b64_ciphertext)

    print("b ciphertext: ", b_ciphertext)

    bank_private_key_path = os.path.join(settings.BASE_DIR, 'key/server_priv_key.pem')
    bank_private_key = RSA.import_key(open(bank_private_key_path).read())
    cipher = PKCS1_v1_5.new(bank_private_key)

    b_lst = cipher.decrypt(base64.standard_b64decode(b64_ciphertext), None)
    
    print("b_lst:", b_lst)
    username, password = parse.unquote(b_lst.decode()).split("&")
    

    print("username: ", username)
    print("password: ", password)

    print("--[Login]--")
    if not all([username, password]):
        return render(request, 'users/login.html', {'errmsg': "inputs shouldn't be null!"})

    passport = Passport.objects.get_one_passport(username=username, password=password)
    if passport is None:
        return render(request, 'users/login.html', {'errmsg': "username or password wrong"})

    request.session['islogin'] = True
    request.session['username'] = username
    request.session['passport_id'] = passport.id
    

    print("--[login success]--")
    return redirect(reverse('home:index'))


def logout(request):
    request.session.flush()
    return redirect(reverse('home:index'))


from payment.models import Payment
import datetime

def check_account(request):
    username = request.session['username']
    passport_id = request.session['passport_id']
    print("user ", username, ": check account")
    passport = Passport.objects.get_passport_by_id(passport_id)
    if passport is not None:
        context = {
            'username': passport.username,
            'account_balance': passport.account_balance,
        }
    else:
        context = None
    
    return render(request, 'users/account.html', context=context)

def get_records(request):
    username = request.POST.get("username")
    context = {}
    payments = Payment.objects.get_payments(username)
    print("payment", payments)
    outrecords = list()
    for item in payments:
        print("payer: ", item.payer)
        print("payee: ", item.payee)
        print("account: ", item.account)
        time = datetime.datetime.strftime(item.create_time, '%Y-%m-%d %H:%M:%S')
        print("time: ", time)
        outrecords.append({'payee': item.payee, 'account': item.account, 
            'time': time})
    context['outrecords'] = outrecords

    income = Payment.objects.get_income(username)
    inrecords = list()
    for item in income:
        print("payer: ", item.payer)
        print("payee: ", item.payee)
        print("account: ", item.account)
        time = datetime.datetime.strftime(item.create_time, '%Y-%m-%d %H:%M:%S')
        print("time: ", time)
        inrecords.append({'payer': item.payer, 'account': item.account, 
            'time': time})
    context['inrecords'] = inrecords
    return JsonResponse(context)

def upload_publickey(request):
    publickey = request.POST.get('publickey')[:-1]
    username = request.session['username']
    
    Passport.objects.set_publickey(username, publickey)
    publickeyPem = Passport.objects.get_one_passport_by_username(username).user_publickey

    print("publickey: ")
    print("last:", publickey[-1].encode())
    print(publickeyPem)
    publickey = RSA.import_key(publickeyPem)
    return JsonResponse({'res': 'pass'})
