from socket import *
# from Crypto.Hash import SHA
# from Crypto import Random
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5

# privatekey_pem = """-----BEGIN RSA PRIVATE KEY-----
# MIIEowIBAAKCAQEAkXLAYu+vT/vcuXn5Mucq4Fl/rTvFV1VL6Eo15crLQ5CGvJBWkk5LxGyHnyrgxykdnhnqaJuKPezYP4SLfgpxlagQA8FavQJX5apWTQaLgEcIiDn8lLqUtrebwPM1IOQkIIWvP7vn32mZYTTT/7GK+KL+sHU/u8ZiqDK+zacOYrbmYlsx7PoXYOycWfPzhOmzXnp8YzNbYciPO7TcYDtHdytQR+tCwwGB07YuZZ4tFmBd0Vr+aqzW22CDg6GQJlt0Gu4Cj2kJFK0KCnzYzJjnwALQLRjCYs6Bxc6yufjoNfk6tUWl1z0EQ1MLvO8XyySzv0dr6XJurFZ+JztaFcTexwIDAQABAoIBAGnwALyPA0vokI3vj1hKE2qxBVOx8zx2/gDE/JjQqlgdzmVNZCDQMlNxER8XZfzpr47WJWvnzjroZWFuMwOsq6prbK6viF2edVLsTEtx9u2Jz2cZhST2+RZUiXdyLUI1qTKe7FQpkuugyHyKs9bLBAOxBHyWCcPE7VrBC0RS5yFyI7XWJFvqQh+OaLBUSCdAlqQs7d8H4mNak3U/xdOcKyGG21X9oqgXKTZ4P713WaP8G5w1LR5BNPAQhgorkIoDpin/Dk+3wkmacGTgTBJQRaa4qZVxnlh7T3WVt+fpYkZVrmLB9tzCi2WatrPn+9ef3OVwR7dHwz9mOd3W9C226dECgYEA6tvF9WBTn7kD28aTKqjQgbNipJEA0JL8dw0jx/0L32Nb9kaeDgPIBjVofCeG0NpqlTbO6OAb5TaNWBBA8ujJj41uv3vpKdKIk0fwcr/PU1OEP11CkPmGGaV4cQNyANYgKATxVJGkSRQaRMZ8qFhrXcdzarsmhHXu5Ms4la0vL70CgYEAnoqNaogsliE39paiM1cfdWkLSFPS4RI84scNnVz2zQh7tyrhqaF+JPmQaVl1W6Mai01j3WdkvveGq6q3K4vInc4jBs1RddA87h+t9J47SZUaDLgi4sRT8AgyZuyBKhIjNT72mEOaz6unnoAfpxCq381jrLRScbsL6o5CGtM//tMCgYEAjHk9c2HVQsCn9SlV1vs4E4vXIXV1lkuEZDTgxPquwkOsuqZMXTeXyVbikvgVZBBwFaW9pn59UOELM7QtFN11yb4fkrqroI9Dj0xFHm1ptX5LqJbAfPQyaF6XpokYBDYO78DdE+c061zxxVcvMoYIWgQ1HY6pICtl40VGKAh5I8UCgYA9KZCC78PbqzcOz3AFxG+jeQHcRlJNeB67EjXDZrDjyokH0eg6681hcFHxAo0O7C56XUHQkWnBbnaq1XJSv1uG3ZaPsjfh7pMC/n+6piyTJ41kKMl0mG8VY+Ql5smxtEuW6BJ0DWi1AzDoKd+MMRbqvi7c2rgPnixrsbP461R99wKBgECq2KadxyWJPYRRt4rrPCxqQQIsVbkFtEp3Fvi7tVAeRiOUUqvoUE4w3HNQSgPbrD3FZAkmAukGi3r43Gi/OamtRLqaCu17oSQrTw2ilYoE8x2q327j9X2m40O4TpI57mMTeKuX87ugaHT75xGMFlKfN+UaO7Of1gxElxnTNAEd
# -----END RSA PRIVATE KEY-----"""

def launch_server():
    # privatekey = RSA.importKey(privatekey_pem)
    # cipher = PKCS1_v1_5.new(privatekey)
    # dsize = SHA.digest_size
    # sentinel = Random.new().read(8+dsize)
    

    with socket(AF_INET, SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', 8080))
        server_socket.listen(5)
        print("server is ready:")
        while True:
            print("-------")
            tmp_socket, CLIENT_ADDR = server_socket.accept()
            print("get connected")
            b_msg = tmp_socket.recv(2048)
            print("b_msg: ", b_msg)
            print("type b_msg", type(b_msg))

            msg = b_msg.decode()
            print("msg", msg)
            print('msg type', type(msg))
            tmp_socket.close()
            # ciphertext, CLIENT_ADDR = server_socket.recvfrom(2048)
            # print("orig cipher: ", ciphertext)
            # print("ciphertext length: ", len(ciphertext))
            # print("dsize: ", dsize)
            # ciphertext = ciphertext.decode()
            # print("decode cipher: ", ciphertext)

            # msg = cipher.decrypt(ciphertext, sentinel)
            # print("msg.len ", len(msg))
            # print("the de msg: ", msg)
            # digest = SHA.new(msg[:-dsize]).digest()
            # if digest == msg[-dsize:]:
            #     print('[pass]: ', msg[:-dsize])
            # else:
            #     print("[wrong]: ", msg[:-dsize])
            # print("[utf-8]: ", msg[:-dsize].decode())
            

if __name__ == "__main__":
    launch_server()
