# coding=utf-8
import json
from datetime import datetime

from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from .compat import quote_plus, encodebytes, b

BEYPAY_URL = "127.0.0.1"


class BeyPay(object):
    @property
    def appid(self):
        return self._appid

    @property
    def app_private_key(self):
        """
        签名用
        """
        if not self._app_private_key:

            if self._app_private_key_path:
                with open(self._app_private_key_path) as fp:
                    self._app_private_key = RSA.importKey(fp.read())
            elif self._app_private_key_string:
                self._app_private_key = RSA.importKey(self._app_private_key_string)
            else:
                raise Exception("App private key is not specified")

        return self._app_private_key

    @property
    def beypay_public_key(self):
        """
        验证签名用
        """
        if not self._beypay_public_key:
            if self._beypay_public_key_path:
                with open(self._beypay_public_key_path) as fp:
                    self._beypay_public_key = RSA.importKey(fp.read())
            elif self._beypay_public_key_string:
                self._beypay_public_key = RSA.importKey(self._beypay_public_key_string)
            else:
                raise Exception("Beypay public key is not specified")

        return self._beypay_public_key

    def __init__(
            self,
            appid,
            app_notify_url,
            app_private_key_path=None,
            app_private_key_string=None,
            beypay_public_key_path=None,
            beypay_public_key_string=None):

        self._appid = str(
            appid)  # namely the app account in the bank, which binds to a CA(you should upload in the bank)


        self._app_notify_url = app_notify_url  #
        self._app_private_key_path = app_private_key_path
        self._app_private_key_string = app_private_key_string
        self._beypay_public_key_path = beypay_public_key_path
        self._beypay_public_key_string = beypay_public_key_string

        self._app_private_key = None
        self._beypay_public_key = None
        self._gateway = BEYPAY_URL

    def build_body(
            self, biz_content, return_url=None, notify_url=None
    ):
        data = {
            "app_id": self._appid,
            "charset": "utf-8",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "biz_content": biz_content
        }

        if return_url is not None:
            data["return_url"] = return_url

        if self._app_notify_url is not None:
            data["notify_url"] = self._app_notify_url
        if notify_url is not None:
            data["notify_url"] = notify_url

        return data

    def _ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def _sign(self, unsigned_string):
        """
        通过如下方法调试签名
        方法1
            key = rsa.PrivateKey.load_pkcs1(open(self._app_private_key_path).read())
            sign = rsa.sign(unsigned_string.encode("utf8"), key, "SHA-1")
            # base64 编码，转换为unicode表示并移除回车
            sign = base64.encodebytes(sign).decode("utf8").replace("\n", "")
        方法2
            key = RSA.importKey(open(self._app_private_key_path).read())
            signer = PKCS1_v1_5.new(key)
            signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
            # base64 编码，转换为unicode表示并移除回车
            sign = base64.encodebytes(signature).decode("utf8").replace("\n", "")
        方法3
            echo "abc" | openssl sha1 -sign alipay.key | openssl base64

        """
        # 开始计算签名
        key = self.app_private_key
        signer = pkcs1_15.new(key)
        signature = signer.sign(SHA256.new(b(unsigned_string)))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self._ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)
        sign = self._sign(unsigned_string)
        ordered_items = self._ordered_data(data)
        quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def api_beypay_trade_page_pay(self, subject, out_trade_no, total_amount,
                                  return_url=None, notify_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
        }

        biz_content.update(kwargs)
        data = self.build_body(
            biz_content,
            return_url=return_url,
            notify_url=notify_url
        )
        return self.sign_data(data)
