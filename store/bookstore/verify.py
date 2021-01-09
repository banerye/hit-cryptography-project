from random import random

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Hash import SHA
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import socket

# def shake_hands(ip, port):
#     client = socket.socket()
#     client.connect((ip, port))
#     # send a randmom string
#     r = ''
#     for i in range(128):
#         r += str(random.randint(0, 9))
#     client.send(r)
#
#     client.recv(1024)




PUBKEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA30Mdr5GbwnuQqjbOL5mm
Qy3F7Q6sQDPuIl8JXJagJMyx99ICEk++kKmsflnxWDe1JUBAIux9CGp6jnk33G7N
C6S7/6VoQJI3hhuWwTtWXcTnasTer++qIjAARjEHFXPL/Y27RMD485Hdy9AMb9UK
SQWuZ1SR5IihvibdwkM7nMHvRIOi+NSw56EYdSc3fH3smHrhDcAjJSZAzffe11gQ
u+RbDkVAV3g7eMQARGKDWZ9lmRqCWxY7NMVtbXWyBfLBY96VFGUB/U181KiM8OLi
LCzcdYLRG1KRmwMIpoPbtlyqs5M+NxCarzPBZnW8BwBzkz6HYaYa1ZD981Tm6LNv
TwIDAQAB
-----END PUBLIC KEY-----"""

#
# message = b'To be encrypted'
# h = SHA.new(message)
# key = RSA.importKey(PUBKEY)
# cipher = PKCS1_v1_5.new(key)
# ciphertext = cipher.encrypt(message+h.digest())
#
# print(ciphertext)

msg = """pmDNYRzB3QTF0FkGsVrrOQ61qwbafcbe99ymHCGtDhKZ8SkC/EzSKpXStQrm0UKv+PF/7OcQfwG5SfZhzDk+htGDQViiagJKmbcI+DnCUdf/iurbC422qYQPjsnPkd3LQXzOt1jLXeq5p9nWrlivRwjAG89SoeiT7EoMXyI/n+f8kTHfxuijPQuoEccxGMUHxmVRQMSXE6Hexxk8Wq4jo9JnBCKIVNplQhT76+P0QObmE9rAbeu47sqi3iJ/YS+Oa+RFzelGFd0lSWaVi4bJ3AsHlMI69iI0NXqyzQ/tt7HvFO1VFylBH99DS+1K+/OLxnPcwVAoPuTqpNfOzAPmAQ==&&/UI0Qui5eQ5j/XifOYFhQw==&&0b5c34436600e3b44edcd3df7f06e0bf74e6d6bbd57e29864a19b9c8f9bb2c71fb040adec775dec0f3151891766d3545011afc65c48d7a715efe92a0bb8ff3d946af002e0d8ae77bfee45bebed8015efed80a061f6ac0d820098a6c13b2b7dd47cf4ea2ef77ffee4e51d23235d600012d3501b0cec3c0d6575235286acde3270a53d87ef747cc4998e9faf40aa3a7435414709ed44fff85e2820e78ff772031e763557e1857d94fe8c591d36f1d6bffdd9865002b36caf97a0496ee1bc0cb9c900119605ef44770d0c21ba52d6622f716fd2a2c78e54b01cc35f1f39f67c391926428f08b2c8b7a7e7a004884ceb1a32f0f09a950e29cd66e996451ad57375f6d17607e218e5164517ad3e633ca5815c3f4d318d377976b6221d4ac302718b8e1fc7c6b34e56483b2e4d8293fe9f36a88bb9a71573d950f87e38feb3b374471bf54586ae2b253971e1618e72daf3081b638989f936d7b9b23ff4f1c074383127bc2630f3e1d3ea47ef2e5ae6393f8b57386899e80d9486786a9015e77552186f5f5f20573a49b84439697f5fe2b408e5f899590e8d184b5c5fce8afd4b1a41181b60f755781c48a397d5fe5a5d0e4b628f1160308e400a002e018df42657a6a759c8e5f495def5fafa2aa07884a98342391026371834c85ab0902a02563b1d0ff71071210e0be629f80e77d4fd4d426e5e1436892b36f02e02c30d938817af7e"""

PRIKEY = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDfQx2vkZvCe5Cq
Ns4vmaZDLcXtDqxAM+4iXwlclqAkzLH30gIST76Qqax+WfFYN7UlQEAi7H0IanqO
eTfcbs0LpLv/pWhAkjeGG5bBO1ZdxOdqxN6v76oiMABGMQcVc8v9jbtEwPjzkd3L
0Axv1QpJBa5nVJHkiKG+Jt3CQzucwe9Eg6L41LDnoRh1Jzd8feyYeuENwCMlJkDN
997XWBC75FsORUBXeDt4xABEYoNZn2WZGoJbFjs0xW1tdbIF8sFj3pUUZQH9TXzU
qIzw4uIsLNx1gtEbUpGbAwimg9u2XKqzkz43EJqvM8FmdbwHAHOTPodhphrVkP3z
VObos29PAgMBAAECggEAXGfWAJW+pxcngBvg6PiqRQHL+tro1kXoGRfGsyiwrap/
OngUXWneENf5Se6GIqIj+oAGS64f7fzMLu3i/fxqJ5iOKzhV1uvtyTbgBag+jd7y
fVFwbdc/TpkZc/PU378mvhIMYV+RapaD+1hn3V2KvUB5t9Db9X/Lmf1SKZZUNQOV
kXqA3IYZkFOZH8+uv6x7k/3U1tkfYxmc2YtWfCX3/BF0o0UJQwHqPDkmwjwUvQhN
VUCUGOAuIOz8vHbQ7iTpNL5c9+71bpZiZ8qauTgE6iTo00G0KV5siq2eFdBAlbkY
HaMUYEtc1POKoEXb9z8xub8BWceweIcjsYf9kSy9EQKBgQD7iRc9NwRJHU3l9WHg
igKAE/K0Ykz6uD1x4/eU0ofph+COtA/csIT+Om9g71yRDv07FmY98J9hXZE3xUSF
+aStbCnZvpRw/nAFIAaMcZLd/0q+P40ON+TaroBj/0hXPxZyW7GKn5ZgK5EqsVpA
NZs+hmPBFb6QbDQYNxBI2V6qeQKBgQDjOY8MwixPTf/d5RjGGiM03jciQODyCvRh
JESs0YOyRMWudyqw9OeUzlQkJ+mAT2/Zid5H7o/3AJ2pRAE3BktsNGn1eodE4lO0
S2bBjvGn8p20Ko3dvPuhpARlaBTAsEzpuqMGagl29dQtx6XlYOx4SRujvMLahuNR
VrhtdpF2BwKBgQDvqRg+WCw6KbSuFVYTpgtp0xfd7Qdhn6fT2xxrbQjYZoF8Fm5C
nOGqhSzYFFiDUd/Pq7Dw9VI2Z/tUQx3d9RWFs1hQwngXDSbYi0ISEKiZ4oNpr42L
bZAdGET2giaAEnklrt4DsbiKmxgusFrIcQsg0NU9BKXUX3RnWhenAY1kKQKBgQCh
93ZjVsl04hl/lv0YwKrV1YwhS3PMtEhMMikNsu6YFPOAEAuLRZcJeCV7/EMyJe2J
d//M8F0IaRT5AbOIAGGkyJu60lM3o8icnJ6rW/Qfjg4hza+AHmSTbLGBgzY/v6uj
c1kfilgixsous8AqB/OnLh2YkkWmtT21zgX6aOj44wKBgA1uDh0IE/Wqu4V8Y+nj
tXhFXXyD7fraufWR99ZN3Tr0rlf6c94T/1RDU8vkCOF83H+MyUO9bacHiwUXvrr+
f/05JA7G4Qp3lkLguFA1Jo+ZvZWuB61Jdk6DusOpZ/M0NXyQN6nMg+kyL0t37cSM
1ULaiOkvis6pAAJS+PU1YxCC
-----END PRIVATE KEY-----
"""

msg_list = msg.split('&&')
if len(msg_list) != 3:
    print("wrong")

# print(msg_list[0])
# Ek(key)
k = RSA.importKey(PRIKEY)
cipher = PKCS1_v1_5.new(k)
key = cipher.decrypt(base64.b64decode(msg_list[0]), None)

# iv, cipher text
iv = base64.b64decode(msg_list[1])
# print(iv)

plaintext = msg_list[2].decode('hex')
print(plaintext)
#
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(plaintext), 16)
