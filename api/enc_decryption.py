import ast
import bcrypt
import jwt
from django.conf import settings
import string
import random

# Password Section
def hash_password(password):
    salt = bcrypt.gensalt(rounds=9)            
    hashed = bcrypt.hashpw(password.encode(settings.ENCODE_ALGORITHM), salt)        
    return hashed

def check_password(password,hashed):         
    if bcrypt.checkpw(password.encode(settings.ENCODE_ALGORITHM), ast.literal_eval(hashed)):        
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