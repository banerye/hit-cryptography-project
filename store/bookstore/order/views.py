# coding=utf-8
import urllib

from django.shortcuts import render,redirect, reverse
import base64
from hashlib import sha256
from utils.decorators import login_required
from django.http import HttpResponse,JsonResponse
from users.models import Address
from books.models import Books
from order.models import OrderInfo, OrderBooks, DSManager, OrderManager, DualSig
from django_redis import get_redis_connection
import datetime
from django.conf import settings
import os
import time

@login_required
def order_place(request):
    '''显示提交订单页面'''
    # 接收数据
    books_ids = request.POST.getlist('books_ids')

    # 校验数据
    if not all(books_ids):
        # 跳转会购物车页面
        return redirect(reverse('cart:show'))

    # 用户收货地址
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)

    # 用户要购买商品的信息
    books_li = []
    # 商品的总数目和总金额
    total_count = 0
    total_price = 0

    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % passport_id

    for books_id in books_ids:
        # 根据id获取商品的信息
        books = Books.objects.get_books_by_id(books_id=books_id)
        # 从redis中获取用户要购买的商品的数目
        count = conn.hget(cart_key, books_id)
        books.count = count
        # 计算商品的小计
        amount = int(count) * books.price
        books.amount = amount
        books_li.append(books)

        # 累计计算商品的总数目和总金额
        total_count += int(count)
        total_price += books.amount

    # 商品运费和实付款
    transit_price = 10
    total_pay = total_price + transit_price

    # 1,2,3
    books_ids = ','.join(books_ids)
    # 组织模板上下文
    context = {
        'addr': addr,
        'books_li': books_li,
        'total_count': total_count,
        'total_price': total_price,
        'transit_price': transit_price,
        'total_pay': total_pay,
        'books_ids': books_ids,
    }

    # 使用模板
    return render(request, 'order/place_order.html', context)

# order/views.py
# 提交订单，需要向两张表中添加信息
# s_order_info:订单信息表 添加一条
# s_order_books: 订单商品表， 订单中买了几件商品，添加几条记录
# 前端需要提交过来的数据: 地址 支付方式 购买的商品id

# 1.向订单表中添加一条信息
# 2.遍历向订单商品表中添加信息
    # 2.1 添加订单商品信息之后，增加商品销量，减少库存
    # 2.2 累计计算订单商品的总数目和总金额
# 3.更新订单商品的总数目和总金额
# 4.清除购物车对应信息

# 事务:原子性:一组sql操作，要么都成功，要么都失败。
# 开启事务: begin;
# 事务回滚: rollback;
# 事务提交: commit;
# 设置保存点: savepoint 保存点;
# 回滚到保存点: rollback to 保存点;
from django.db import transaction

@transaction.atomic
def order_commit(request):
    '''生成订单'''
    # 验证用户是否登录
    if not request.session.has_key('islogin'):
        return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

    # 接收数据
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    books_ids = request.POST.get('books_ids')
    
    # 进行数据校验
    if not all([addr_id, pay_method, books_ids]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

    try:
        addr = Address.objects.get(id=addr_id)
    except Exception as e:
        # 地址信息出错
        return JsonResponse({'res': 2, 'errmsg': '地址信息错误'})

    if int(pay_method) not in OrderInfo.PAY_METHODS_ENUM.values():
        return JsonResponse({'res': 3, 'errmsg': '不支持的支付方式'})
    
    # 订单创建
    # 组织订单信息
    passport_id = request.session.get('passport_id')
    
    # 订单id: 20171029110830+用户的id
    try:
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    except Exception as e:
        print(e)
    # 运费
    transit_price = 10
    # 订单商品总数和总金额
    total_count = 0
    total_price = 0
    
    # 创建一个保存点
    sid = transaction.savepoint()
    try:
        # 向订单信息表中添加一条记录
        order = OrderInfo.objects.create(order_id=order_id,
                                 passport_id=passport_id,
                                 addr_id=addr_id,
                                 total_count=total_count,
                                 total_price=total_price,
                                 transit_price=transit_price,
                                 pay_method=pay_method)

        # 向订单商品表中添加订单商品的记录
        books_ids = books_ids.split(',')
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' % passport_id

        # 遍历获取用户购买的商品信息
        for id in books_ids:
            books = Books.objects.get_books_by_id(books_id=id)
            if books is None:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 4, 'errmsg': '商品信息错误'})

            # 获取用户购买的商品数目
            count = conn.hget(cart_key, id)

            # 判断商品的库存
            if int(count) > books.stock:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 5, 'errmsg': '商品库存不足'})

            # 创建一条订单商品记录
            OrderBooks.objects.create(order_id=order_id,
                                      books_id=id,
                                      count=count,
                                      price=books.price)

            # 增加商品的销量，减少商品库存
            books.sales += int(count)
            books.stock -= int(count)
            books.save()

            # 累计计算商品的总数目和总额
            total_count += int(count)
            total_price += int(count) * books.price

        # 更新订单的商品总数目和总金额
        order.total_count = total_count
        order.total_price = total_price
        order.save()

    except Exception as e:
        # 操作数据库出错，进行回滚操作
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res': 7, 'errmsg': '服务器错误'})

    # 清除购物车对应记录
    conn.hdel(cart_key, *books_ids)

    # 事务提交
    transaction.savepoint_commit(sid)
    # 返回应答
    return JsonResponse({'res': 6})

from alipay import AliPay
from beypay import BeyPay
from users.models import Passport
import datetime



from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import urllib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

@login_required
def order_pay(request):
    '''订单支付'''

    # 接收订单id
    order_id = request.POST.get('order_id')
    total = str(request.POST.get('total')).replace('元','CYN')
    OI = str(request.POST.get('OI'))

    # 数据校验
    if not order_id:
        return JsonResponse({'res': 1, 'errmsg': '订单不存在'})
    # print("success")
    try:
        order = OrderInfo.objects.get(order_id=order_id,
                                      status=1,
                                      pay_method=1)  #secret payment
    except OrderInfo.DoesNotExist:
        return JsonResponse({'res': 2, 'errmsg': '订单信息出错'})

    # print("success")
    # # 将app_private_key.pem和app_public_key.pem拷贝到order文件夹下。
    # app_private_key_path = os.path.join(settings.BASE_DIR, 'order/app_private_key.pem')
    # alipay_public_key_path = os.path.join(settings.BASE_DIR, 'order/app_public_key.pem')
    # # print("success")
    # app_private_key_string = open(app_private_key_path).read()
    # alipay_public_key_string = open(alipay_public_key_path).read()

    # now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    # 订单号、我的bank账号、交易金额、当前时间
    # OI:


    tmp = settings.MY_ACCOUNT + '&&' + str(order_id) + '&&' + total + '&&' + urllib.quote(OI, safe="~()*!.'")
    a = Passport.objects.get_passport_by_id(request.session['passport_id'])
    pKey = str(a.pubkey)
    pKey = pKey.replace('\\n','\n')
    # pubKey = '-----BEGIN PUBLIC KEY-----\nMIIBCgKCAQEAwcQS+goKQ3q0csFggZy+6jtJ/4lQ2JeLsuhY2CmQ2Ss+meKmWLPtfQPhgDgo\n1/7BQDSWXdYSsB/zCPrHIYdSyZeDmx720k9/LqnqAecstDEGM8uH+NHuTDONGERFUNcxkNXr\n85BD7j3EQfuWNFew2K0vDjcd7W/LdNWMxTYckoNuomLR91uGfklUWyjTKx4QtDARv9BDFMEf\n4VuRBqoIGFX96XqjyGwxfiA9aHdIG3l+v20/xpB1NVEa8LCWZ2LoxE5sPQgiW4WtdaRoHm2R\nDSU0ldbA3rsxFSwSXrJ+YJGKVLxyEBVUYZZPD9NyAz6bdKYQnt+/a531YhLXFMlzRwIDAQAB\n-----END PUBLIC KEY-----\n'
    key = RSA.importKey(pKey)
    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(tmp)
    ciphertext = base64.b64encode(ciphertext)
    pay_url = settings.BEYPAY_URL + ciphertext
    # print("success")

    # print(pay_url)
    return JsonResponse({'res': 3, 'pay_url': pay_url, 'message': 'OK'})



# #私钥文件
# priKey = "-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAwcQS+goKQ3q0csFggZy+6jtJ/4lQ2JeLsuhY2CmQ2Ss+meKmWLPtfQPh\ngDgo1/7BQDSWXdYSsB/zCPrHIYdSyZeDmx720k9/LqnqAecstDEGM8uH+NHuTDONGERFUNcx\nkNXr85BD7j3EQfuWNFew2K0vDjcd7W/LdNWMxTYckoNuomLR91uGfklUWyjTKx4QtDARv9BD\nFMEf4VuRBqoIGFX96XqjyGwxfiA9aHdIG3l+v20/xpB1NVEa8LCWZ2LoxE5sPQgiW4WtdaRo\nHm2RDSU0ldbA3rsxFSwSXrJ+YJGKVLxyEBVUYZZPD9NyAz6bdKYQnt+/a531YhLXFMlzRwID\nAQABAoIBAAGctkOR+IEzbptVaBLONJy3VPKplPS47uUj7xDAZDJf4wLvc5VqYu5SaxUIZv/5\nNEVh5jbK90hbPVmybmMGX5dOsWF0BkIvJdUX3vV9/bL8c12fTT2XmqkanNZL2b1yNTBMK8QX\nZlRTblbnuFC6923RH3nCfg1bKrr8KLNM37cWjGNq64WFM+d9/DratrnHqX6cBT42WhstgFLV\nAamwqxoTBZg6HtXCnXTJcS+2GMZCPUtUr94p14B4v64T71z26SoLjSJVpUK7nNXGR16k8OYX\n9wbjJ/nAoPxVl2MjGNipdUXYMeci+AfXWjMSXPRMNev/7DB7HscYoTnVSEWMSxECgYEA7QLS\n1g57SUXRXhhO/hKSJrYJoU90gEdkFEJ89d3Qzm1BRZ72icNHpcbWceUAGOwSfO8WSdkYnLSL\nEBq3AGY7Z6Wzut+TV47xa4qAJaNGSZeUo9vU13L+50S15DkijkACqaGBK2YbVgN93ANtQ6rT\nNLFQkdU51lW8S9HC834UPf8CgYEA0UpHUrAE84I2uG3LggH5jEqpUTrp6iLZRc9c+S7o4XoZ\nXBcJ4FhrUg45Nq3H3rQdcVUmCm251ARjN4jidHmq7sYJgTkuuJYxvRDwRe7fraU9u7rP2rci\n45SdS2owBlKJeAIUffCvvHQL3hILSFe18mCOPy9hpg7C3W1U15+jWrkCgYB2A/bp4XIgLSSw\nftguiR6/KdunuAGhsmqx7917K8VCVIKw4ROPy24MrPKw6b9fqYUXMpHdmb04ommwTi0bhMxF\nsuvIvHUIn0O1MdTXaPKhyFmaMedMlJU6oSsVBiIfxN3Oi33fF0u7S6fK+uXYUOI0FaqxwwO2\npyBIfJ1fU0NPDwKBgEawyBZtzb5SJRl2PF7VO+ze6wG83HVw/+JMgCLKbW57R0WLopJcSyOU\nGk8Vs4TNYYR+NjMfjLzIHpsLaTHeRpYP3fX/0oAWewZZSk7UuEh2n7thBgPiB67G67olS8NW\n7YfTbAh9213T9I41mgn9Vj9fzawZ3Omx4q/X1ehey1ZBAoGAYWwbHFu6zsdZJ3i89i6uJfcC\nzte1ntDinRTgeSML8EKgq5aF2Gnrhw4reODs+aMCpVRX9VnjZ/W4ZLiiPJqXkEmhgNWneMJ+\nlgZsLv3ReFqQp8JNmtgx8yBDHxyrei5XMDgf6qHJ2pULIv1OccY9C4scHY7aX6G+Q9gF50eG\n9o8=\n-----END RSA PRIVATE KEY-----\n"
#
#
# #公钥文件
# pubKey = "-----BEGIN PUBLIC KEY-----\nMIIBCgKCAQEAwcQS+goKQ3q0csFggZy+6jtJ/4lQ2JeLsuhY2CmQ2Ss+meKmWLPtfQPhgDgo\n1/7BQDSWXdYSsB/zCPrHIYdSyZeDmx720k9/LqnqAecstDEGM8uH+NHuTDONGERFUNcxkNXr\n85BD7j3EQfuWNFew2K0vDjcd7W/LdNWMxTYckoNuomLR91uGfklUWyjTKx4QtDARv9BDFMEf\n4VuRBqoIGFX96XqjyGwxfiA9aHdIG3l+v20/xpB1NVEa8LCWZ2LoxE5sPQgiW4WtdaRoHm2R\nDSU0ldbA3rsxFSwSXrJ+YJGKVLxyEBVUYZZPD9NyAz6bdKYQnt+/a531YhLXFMlzRwIDAQAB\n-----END PUBLIC KEY-----\n"


# def sign(data):
#     key = RSA.importKey(priKey)
#     h = SHA256.new(data)
#     signer = PKCS1_v1_5.new(key)
#     signature = signer.sign(h)
#     return base64.b64encode(signature)

def my_verify(data, signature, pubKey):
    key = RSA.importKey(pubKey)
    # print(pubKey)
    h = SHA256.new(data)
    verifier = pkcs1_15.new(key)
    print('cc')
    try:
        verifier.verify(h, base64.standard_b64decode(signature))
        return True
    except Exception as e:
        print(e)
    return False

import socket
from time import sleep


def send_to_bank(sock, data):
    try:
        # sock.connect((settings.BANK_IP, settings.BANK_PORT))
        sock.send(data)
        print("send to bank successfully")
        # print(sock.recv(2048))

    except Exception as e:
        return True

@login_required
def check_pay(request):
    '''获取用户支付的结果'''

    # receive data from bank
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(5)
    print("server is ready:")
    while True:
        print("-------")
        tmp_socket, CLIENT_ADDR = server_socket.accept()
        sleep(1)
        try:
            msg = tmp_socket.recv(2048)
            print(msg)
            break
        except Exception as e:
            continue

    # connect to bank
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.settimeout(1)
    # print('ss')
    msg_list = msg.split('&&')
    if len(msg_list) != 3:
        if send_to_bank(tmp_socket, 'NO'):
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
        return JsonResponse({'res': 0, 'errmsg': '订单格式错误'})

    # Ek(key), iv, cipher text
    k = RSA.importKey(settings.PRIKEY)
    cipher = PKCS1_v1_5.new(k)
    key = cipher.decrypt(base64.b64decode(msg_list[0]), None)
    iv = base64.b64decode(msg_list[1])
    plaintext = msg_list[2].decode('hex')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(plaintext), 16)

    # verify infomation
    try:
        tmp = pt.split("&&", 2)
    except:
        if send_to_bank(tmp_socket, 'NO'):
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
        return JsonResponse({'res': 0, 'errmsg': '订单格式错误'})
    OI = urllib.unquote(tmp[0])
    PI_hash = tmp[1]
    DS = tmp[2]
    # print("DS:"+DS)
    try:
        OI_info = OI.split("AAAAA", 3)
    except:
        if send_to_bank(tmp_socket, 'NO'):
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
        return JsonResponse({'res': 0, 'errmsg': '订单格式错误'})

    order_id = OI_info[1]
    # print(order_id)
    # 数据校验
    if not order_id:
        if send_to_bank(tmp_socket, 'NO'):
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
        return JsonResponse({'res': 1, 'errmsg': '订单不存在'})

    try:
        order = OrderInfo.objects.get(order_id=order_id,
                                      status=1,
                                      pay_method=1)  # secret payment
    except OrderInfo.DoesNotExist:
        if send_to_bank(tmp_socket, 'NO'):
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
        return JsonResponse({'res': 2, 'errmsg': '订单信息出错'})
    # verify DS
    sh = sha256()
    try:
        sh.update(base64.b64encode(OI))
    except Exception as e:
        if send_to_bank(tmp_socket, 'NO'):
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
        return JsonResponse({'res': 5, 'errmsg': '编码错误'})
    OI_hash = sh.hexdigest()
    # print("OI_hash:"+OI_hash)
    # plaintext m = sha256(OI_hash+PI_hash)
    # print("PI_hash:" + PI_hash)
    sh = sha256()
    sh.update(OI_hash+PI_hash)
    m = sh.hexdigest()
    # print(m)
    # get user PUBkey
    a = Passport.objects.get_passport_by_id(request.session['passport_id'])

    pKey = str(a.pubkey)
    pKey = pKey.replace('\\n', '\n')
    try:
        if not my_verify(m, DS, pKey):
            if send_to_bank(tmp_socket, 'NO'):
                return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})
            return JsonResponse({'res': 6, 'errmsg': '签名错误'})
    except Exception as e:
        print(e)

    # after verify, listen to bank, watch if paid
    print("suc")
    # back_url = "http://localhost:8000/user/order/"
    send_to_bank(tmp_socket, 'YES')
    # return JsonResponse({'res': 3, 'errmsg': '支付成功'})
    while True:
        print("-------")
        sleep(1)
        try:
            msg = tmp_socket.recv(2048)
            print(msg)
            if msg == '10000':
                return JsonResponse({'res': 7, 'errmsg': '银行验证出错'})
            elif msg == '20000':
                print('aaa')
                return JsonResponse({'res': 3, 'errmsg': '支付成功', 'data': DS})
            else:
                return JsonResponse({'res': 4, 'errmsg': '支付出错'})
        except Exception as e:
            return JsonResponse({'res': 7, 'errmsg': '银行网络错误'})

@login_required
def after_pay(request):
    DS = request.POST.get('DS')
    order_id = request.POST.get('order_id')
    print('cc')
    # change database
    try:
        DualSig.objects.add_one_DS(DS)
        OrderInfo.objects.change_one_state(order_id, 2)
    except Exception as e:
        print(e)
    print('cc')
    return JsonResponse({'res':3})
    # return render(request, 'order/bankpay.html')


