#!/usr/bin/env python

from Crypto.Cipher import AES
from django.conf import settings

def encryptData(plainText):            
    cipher=AES.new(settings.AES_KEY.encode(settings.ENCODE_ALGORITHM), AES.MODE_EAX)     
    ciphertext,tag=cipher.encrypt_and_digest(plainText.encode())                        
    return {"cipherText":str(ciphertext),"tag":str(tag)}

def decryptData(ciphertext,tag):                  
    cipher=AES.new(settings.AES_KEY.encode(settings.ENCODE_ALGORITHM), AES.MODE_EAX)         
    plainText=cipher.decrypt_and_verify(bytes(ciphertext),bytes(tag)).decode()    
    return plainText    