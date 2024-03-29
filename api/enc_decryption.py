import ast
import hashlib
import bcrypt
import jwt
from django.conf import settings
import string
import random
from django.utils.timezone import now as getTimeNow

# Password Section
def hash_password(password):    
    salt = bcrypt.gensalt(rounds=9)            
    sha_password=hashlib.sha256(password.encode(settings.ENCODE_ALGORITHM)).digest()    
    hashed = bcrypt.hashpw(sha_password,salt)        
    return hashed

def check_password(password,hashed):     
    sha_password=hashlib.sha256(password.encode(settings.ENCODE_ALGORITHM)).digest()    
    if bcrypt.checkpw(sha_password, ast.literal_eval(hashed)):        
        return True
    else:        
        return False  

def generate_random_password():	
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length = 8
    random.shuffle(characters)
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    
    random.shuffle(password)
    return "".join(password)

# Token Section
def encode_value(payload):
    encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded

def decode_value(encoded):    
    decoded = jwt.decode(encoded, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])                                         
    return decoded

# Encrypt Data Section
def encrypt_value(plainText):
    now = getTimeNow()
    payload = {'plainText': plainText,'createdAt': now.strftime("%m/%d/%Y, %H:%M:%S")}
    cipher = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return cipher

def decrypt_value(encoded):    
    plainText = jwt.decode(encoded, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])                                         
    return plainText["plainText"]