from mongoengine import *
import datetime

# Create your models here.
class Administrators(Document):
    '''
    Primary key is automatically generated as _id
    '''    
    username=StringField(required=True)
    password=StringField(required=True)
    token=StringField()
    name=StringField(required=True)
    email=StringField(required=True)
    phone_no=StringField(required=True)
    admin=BooleanField(default=True)
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)

class Doctors(Document):
    '''
    Primary key is automatically generated as _id
    '''
    administrator_id=ReferenceField(Administrators, reverse_delete_rule=CASCADE)    
    username=StringField(required=True)
    password=StringField(required=True)
    token=StringField()
    name=StringField(required=True)
    email=StringField(required=True)
    phone_no=StringField(required=True)
    gender=StringField(required=True)    
    specialization=StringField(required=True)
    status=StringField(required=True)
    fee=IntField(required=True)
    date_of_birth=StringField(required=True)
    doctor=BooleanField(default=True)
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)

class Nurses(Document):
    '''
    Primary key is automatically generated as _id
    '''
    administrator_id=ReferenceField(Administrators, reverse_delete_rule=CASCADE)    
    username=StringField(required=True)
    password=StringField(required=True)
    token=StringField()
    name=StringField(required=True)
    email=StringField(required=True)
    phone_no=StringField(required=True)
    gender=StringField(required=True)    
    specialization=StringField(required=True)
    status=StringField(required=True)
    date_of_birth=StringField(required=True)
    nurse=BooleanField(default=True)
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)   

class Pharmacists(Document):
    '''
    Primary key is automatically generated as _id
    '''
    administrator_id=ReferenceField(Administrators, reverse_delete_rule=CASCADE)    
    username=StringField(required=True)
    password=StringField(required=True)
    token=StringField()        
    name=StringField(required=True)
    email=StringField(required=True)
    phone_no=StringField(required=True)
    gender=StringField(required=True)        
    status=StringField(required=True)
    date_of_birth=StringField(required=True)
    pharmacist=BooleanField(default=True)
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)

class Patients(Document):
    '''
    Primary key is automatically generated as _id
    '''        
    name=StringField(required=True)
    email=StringField(required=True)
    phone_no=StringField(required=True)
    gender=StringField(required=True)
    weight=IntField(default=0)
    height=IntField(default=0)
    date_of_birth=StringField(required=True)
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)    

class Admissions(Document):
    '''
    Primary key is automatically generated as _id
    '''
    patient_id=ReferenceField(Patients, reverse_delete_rule=CASCADE)
    doctor_id=ReferenceField(Patients, reverse_delete_rule=CASCADE)
    nurse_id=ReferenceField(Patients, reverse_delete_rule=CASCADE)
    symptoms=StringField(required=True)
    treated=BooleanField(default=False)    
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)

class MedicalRecords(Document):
    '''
    Primary key is automatically generated as _id
    '''
    admission_id=ReferenceField(Admissions, reverse_delete_rule=CASCADE)    
    diagnosis=StringField()
    notes=StringField()
    prescription=StringField()    
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)

class Payments(Document):
    '''
    Primary key is automatically generated as _id
    '''
    admission_id=ReferenceField(Admissions, reverse_delete_rule=CASCADE)    
    pharmacist_id=ReferenceField(Pharmacists, reverse_delete_rule=CASCADE)        
    amount_paid=IntField(required=True)
    method_used=StringField(required=True)    
    created_at=DateTimeField(required=True)
    updated_at=DateTimeField(default=datetime.datetime.utcnow)    