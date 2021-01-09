# coding=utf-8
from hashlib import sha256

def get_hash(str):
    '''取一个字符串的hash值'''
    sh = sha256()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()
