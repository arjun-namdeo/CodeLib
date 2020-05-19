'''
Created on June 20, 2014

@author: Arjun Prasad Namdeo
@version: v01
'''


import base64

key = "a765%$#@z,;]{&"

def encrypt(clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))

def decrypt(enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


'''
A = encrypt('arjun')
print A
print decrypt('wqmgqpM=') 
'''

