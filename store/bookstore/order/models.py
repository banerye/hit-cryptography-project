# coding=utf-8
from django.db import models
from db.base_model import BaseModel
class OrderManager(models.Manager):
    def change_one_state(self, order_id, value):
        print("OID:"+order_id)
        order = self.get(order_id=order_id)
        order.status = value
        order.save()


class OrderInfo(BaseModel):
    '''订单信息模型类'''

    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "微信支付"),
        (3, "支付宝"),
        (4, "银联支付")
    )

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "WEIXIN": 2,
        "ALIPAY": 3,
        "UNIONPAY": 4,
    }

    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
    )

    order_id = models.CharField(max_length=64, primary_key=True, verbose_name='订单编号')
    passport = models.ForeignKey('users.Passport', verbose_name='下单账户')
    addr = models.ForeignKey('users.Address', verbose_name='收货地址')
    total_count = models.IntegerField(default=1, verbose_name='商品总数')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单运费')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='支付方式')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付编号')

    class Meta:
        db_table = 's_order_info'

    objects = OrderManager()

class OrderBooks(BaseModel):
    '''订单商品模型类'''
    order = models.ForeignKey('OrderInfo', verbose_name='所属订单')
    books = models.ForeignKey('books.Books', verbose_name='订单商品')
    count = models.IntegerField(default=1, verbose_name='商品数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')

    class Meta:
        db_table = 's_order_books'




import datetime

class DSManager(models.Manager):
    def add_one_DS(self, DS):
        '''添加一个DS'''
        passport = self.create(DS=DS, time=datetime.datetime.now().strftime('%Y-%m-%d'))

        return passport

class DualSig(BaseModel):
    '''双重签名类'''
    DS = models.CharField(max_length=1000, verbose_name='双重签名')
    time = models.CharField(max_length=30, verbose_name='交易时间')

    class Meta:
        db_table = 's_dual_sig'

    objects = DSManager()
