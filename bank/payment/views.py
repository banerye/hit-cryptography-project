from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64
from urllib import parse
from socket import socket, AF_INET, SOCK_STREAM
from users.models import Passport
from payment.models import Payment
import os
from django.conf import settings


# Create your views here.

# to change maybe
SERVER_ADDR = ("172.20.24.179", 8080)

def detail(request, ciphertext):
    return render(request, 'payment/detail.html')


bank_private_key_path = os.path.join(settings.BASE_DIR, 'key/server_priv_key.pem')
bankPrivateKey = RSA.import_key(open(bank_private_key_path).read())
cipher = PKCS1_v1_5.new(bankPrivateKey)

def check(request):
    print("hellod fdk dl")
    ciphertext = request.POST.get("data")
    toBank, toStore = ciphertext.split("&&&")
    PI, OI_hash, dual_sig = aes_decrypt(toBank)
    # to analyse PI
    username, passwd_hash, payee_username, money, timestamp = PI.split("AAA")
    
    money = eval(money[:-3])
    payer_passport = Passport.objects.get_one_passport(username, passwd_hash)
    if payer_passport is None:
        # TODO: add response logic
        return JsonResponse({'tip': 'password uncorrect'})

    
    payee_passport = Passport.objects.get_one_passport_by_username(payee_username)
    if payer_passport.account_balance < money:
        return JsonResponse({'tip': 'insufficient balance'})
    
    print("[HHHHHHHHH]")
    userPublicKeyPem = Passport.objects.get_user_publickey_by_id(payer_passport.id)
    print("userPublicKeyPem: ", userPublicKeyPem)
    print("length: ", len(userPublicKeyPem))
    user_publickey = RSA.import_key(userPublicKeyPem)

    if not check_dual_sign(PI, OI_hash, dual_sig, user_publickey):
        return JsonResponse({"tip": "bank verify error"})
    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)
        client_socket.send(toStore.encode())
        ret_msg = client_socket.recv(2048)
        print("ret_msg: ", ret_msg)
        
        if ret_msg == 'No':
            return JsonResponse({"tip": "store verify wrong"})
        
        if not Payment.objects.add_one_payment(payer_passport, payee_passport, money, dual_sig):
            client_socket.send("10000".encode())
        
        client_socket.send("20000".encode())
    return JsonResponse({'tip': "pay ok"})


def aes_decrypt(toBank):
    encryptedKeyToBank, ivToBank, bankCiphertext = toBank.split('&&')
    b_keyToBank = cipher.decrypt(base64.standard_b64decode(encryptedKeyToBank), None)

    cipherAES = AES.new(b_keyToBank, AES.MODE_CBC, 
        iv=base64.standard_b64decode(ivToBank))
    b_ciphertextToBank = bytes.fromhex(bankCiphertext)
    b_plaintextToBank = unpad(cipherAES.decrypt(b_ciphertextToBank), 16)
    plaintext = b_plaintextToBank.decode("ascii")
    PI, OI_hash, dual_sig = plaintext.split("&&")
    PI = parse.unquote(PI)
    return PI, OI_hash, dual_sig

def check_dual_sign(PI, OI_hash, dual_sig, user_publickey):
    b64_PI = base64.standard_b64encode(PI.encode())
    hash_object = SHA256.new(data=b64_PI)
    PI_hash = hash_object.hexdigest()
    my_sig = SHA256.new(data=(OI_hash + PI_hash).encode())
    OI_PI_hash = my_sig.hexdigest()
    OI_PI_d_hash = SHA256.new(OI_PI_hash.encode())
    b_dual_sig = base64.standard_b64decode(dual_sig)

    try:
        pkcs1_15.new(user_publickey).verify(OI_PI_d_hash, b_dual_sig)
        return True
    except (ValueError, TypeError):
        return False
