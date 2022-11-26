from mongoengine import *
import datetime

# Create your models here.
class Patients(Document):
    '''
    Primary key is automatically generated as _id
    '''    
    name=StringField()
    email=StringField()
    phone_no=StringField()
    gender=StringField()
    weight=IntField(default=0)
    height=IntField(default=0)
    date_of_birth=DateTimeField()
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)
    

class Doctors(Document):
    '''
    Primary key is automatically generated as _id
    '''
    username:StringField()
    password:StringField()
    token:StringField()
    name=StringField()
    email=StringField()
    phone_no=StringField()
    gender=StringField()    
    specialization:StringField()
    status=StringField()
    fee=IntField()
    date_of_birth=DateTimeField()
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)

class Nurses(Document):
    '''
    Primary key is automatically generated as _id
    '''
    username:StringField()
    password:StringField()
    token:StringField()
    name=StringField()
    email=StringField()
    phone_no=StringField()
    gender=StringField()    
    specialization:StringField()
    status=StringField()
    date_of_birth=DateTimeField()
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)   

class Pharmacists(Document):
    '''
    Primary key is automatically generated as _id
    '''
    username:StringField()
    password:StringField()
    token:StringField()
    name=StringField()
    email=StringField()
    phone_no=StringField(max_length=10)
    gender=StringField()        
    status=StringField()
    date_of_birth=DateTimeField()
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)

class Admissions(Document):
    '''
    Primary key is automatically generated as _id
    '''
    patient_id=ReferenceField(Patients, reverse_delete_rule=CASCADE)
    doctor_id=ReferenceField(Patients, reverse_delete_rule=CASCADE)
    nurse_id=ReferenceField(Patients, reverse_delete_rule=CASCADE)
    symptoms:StringField()
    treated=BooleanField(default=False)    
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)

class MedicalRecords(Document):
    '''
    Primary key is automatically generated as _id
    '''
    admission_id=ReferenceField(Admissions, reverse_delete_rule=CASCADE)    
    diagnosis:StringField()
    notes:StringField()
    prescription:StringField()    
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)

class Payments(Document):
    '''
    Primary key is automatically generated as _id
    '''
    admission_id=ReferenceField(Admissions, reverse_delete_rule=CASCADE)    
    pharmacist_id=ReferenceField(Pharmacists, reverse_delete_rule=CASCADE)        
    amount_paid:IntField()
    method_used:StringField()    
    created_at:DateTimeField()
    updated_at:DateTimeField(default=datetime.datetime.utcnow)    