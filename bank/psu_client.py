from socket import *
from time import sleep
# from Crypto.Cipher import PKCS1_v1_5
# from Crypto.Hash import SHA
# from Crypto.PublicKey import RSA

# publickey_pem = """-----BEGIN PUBLIC KEY-----
# MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkXLAYu+vT/vcuXn5Mucq4Fl/rTvFV1VL6Eo15crLQ5CGvJBWkk5LxGyHnyrgxykdnhnqaJuKPezYP4SLfgpxlagQA8FavQJX5apWTQaLgEcIiDn8lLqUtrebwPM1IOQkIIWvP7vn32mZYTTT/7GK+KL+sHU/u8ZiqDK+zacOYrbmYlsx7PoXYOycWfPzhOmzXnp8YzNbYciPO7TcYDtHdytQR+tCwwGB07YuZZ4tFmBd0Vr+aqzW22CDg6GQJlt0Gu4Cj2kJFK0KCnzYzJjnwALQLRjCYs6Bxc6yufjoNfk6tUWl1z0EQ1MLvO8XyySzv0dr6XJurFZ+JztaFcTexwIDAQAB
# -----END PUBLIC KEY-----"""

SERVER_ADDR = ('172.20.76.44', 8080)

def launch_client():
    # publickey = RSA.importKey(publickey_pem)
    # cipher = PKCS1_v1_5.new(publickey)
    while True:
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            sleep(3)
            client_socket.connect(SERVER_ADDR)
            client_socket.send("I am Banerye~".encode())
            print("send successfully")
            # msg = input(">>>").encode()
            
            # h = SHA.new(msg)
            
            # ciphertext = cipher.encrypt(msg + h.digest())
            # print("ciphertext: ", ciphertext)
            


if __name__ == "__main__":
    launch_client()