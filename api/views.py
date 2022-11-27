import traceback
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.response import Response
from rest_framework import status

from .permissions import isAuthorized
from .models import *
from .enc_decryption import decode_value, decrypt_value, encrypt_value, hash_password,check_password,encode_value
from .serializers import *
from django.utils.timezone import now as getTimeNow
from .Helpers import checkUsernameTaken

import logging
logger = logging.getLogger("django")

# HTTP Statuses
statusOk = status.HTTP_200_OK
statusCreated = status.HTTP_201_CREATED
statusBadRequest = status.HTTP_400_BAD_REQUEST
statusNoContent = status.HTTP_204_NO_CONTENT
statusNotFound = status.HTTP_404_NOT_FOUND
statusExists = status.HTTP_423_LOCKED

# Create your views here.
@api_view(['POST'])
@permission_classes([isAuthorized])
def register_user(request):
    data = json.loads(request.body)
    try:
        username = data['username']        
        password = data['password']
        name=encrypt_value(data["name"])
        email=encrypt_value(data["email"])
        phone_no=encrypt_value(data["phone_no"])
        user_type=data["user_type"]

        gender=None
        status=None
        date_of_birth=None
        fee=None
        specialization=None
        administrator_id=None

        if user_type=="doctor" or user_type=="nurse" or user_type=="pharmacist":
            gender=data["gender"]
            status=data["status"]
            date_of_birth=encrypt_value(data["date_of_birth"])
            administrator_id=data["administrator_id"]

        if user_type=="doctor" or user_type=="nurse":            
            specialization=data["specialization"]

        if user_type=="doctor":
            fee=data["fee"]        
        
        if(username):
            username = username.lower()
        if(username and password):
            taken=checkUsernameTaken(username)
            if taken==True:            
                return Response('Username is already taken', status=statusExists)
            else:            
                hashed_password = hash_password(password)
                new_user=None
                if user_type=="admin":
                    new_user = Administrators(
                            username=username,
                            password=str(hashed_password),
                            name=name,
                            email=email,
                            phone_no=phone_no,
                            created_at=getTimeNow()
                            )
                elif user_type=="doctor":
                    new_user = Doctors(
                            administrator_id=administrator_id,
                            username=username,
                            password=str(hashed_password),
                            name=name,
                            email=email,
                            phone_no=phone_no,
                            gender=gender,
                            specialization=specialization,
                            status=status,
                            fee=fee,
                            date_of_birth=date_of_birth,
                            created_at=getTimeNow()
                            )     
                elif user_type=="nurse":
                    new_user = Nurses(
                            administrator_id=administrator_id,
                            username=username,
                            password=str(hashed_password),
                            name=name,
                            email=email,
                            phone_no=phone_no,
                            gender=gender,
                            specialization=specialization,
                            status=status,                            
                            date_of_birth=date_of_birth,
                            created_at=getTimeNow()
                            )     
                elif user_type=="pharmacist":
                    new_user = Pharmacists(
                            administrator_id=administrator_id,
                            username=username,
                            password=str(hashed_password),
                            name=name,
                            email=email,
                            phone_no=phone_no,
                            gender=gender,                            
                            status=status,                            
                            date_of_birth=date_of_birth,
                            created_at=getTimeNow()
                            )                                                                                   
                new_user.save()                
                return Response('Successfully created an account for the new '+user_type.title()+' account', status=statusCreated)
        else:
            return Response('Please make sure to fill in everything in the form', status=statusBadRequest)
    except:
        logger.error(traceback.format_exc())
        return Response('An error occured while creating the new account', status=statusBadRequest)

@api_view(['POST'])
def login_user(request):
    data = json.loads(request.body)
    try:
        username = data['username']
        password = data['password']
        if(username):
            username = username.lower()
        if(username and password):
            try:
                profile = Administrators.objects.get(username=username)               
                if(check_password(password, profile.password) == True):                    
                    now = getTimeNow()                    
                    payload = {'username': username,'loggedinAt': now.strftime("%m/%d/%Y, %H:%M:%S")}                    
                    profile.token=encode_value(payload)                                         
                    serialised_profile = AdministratorsSerializer(profile, many=False)                                        
                    return Response(serialised_profile.data, status=status.HTTP_200_OK)
                else:
                    return Response('Invalid login credentials', status=statusBadRequest)
            except Administrators.DoesNotExist:
                try:
                    profile = Doctors.objects.get(username=username)
                    if(check_password(password, profile.password) == True):
                        now = getTimeNow()
                        payload = {'username': username, 'loggedinAt': now.strftime("%m/%d/%Y, %H:%M:%S")}
                        profile.token=encode_value(payload)                        
                        serialised_profile = DoctorsSerializer(profile, many=False)                        
                        return Response(serialised_profile.data, status=status.HTTP_200_OK)
                    else:
                        return Response('Invalid login credentials', status=statusBadRequest)
                except Doctors.DoesNotExist:
                    try:
                        profile = Pharmacists.objects.get(username=username)
                        if(check_password(password, profile.password) == True):
                            now = getTimeNow()
                            payload = {'username': username, 'loggedinAt': now.strftime("%m/%d/%Y, %H:%M:%S")}
                            profile.token=encode_value(payload)                                                    
                            serialised_profile = PharmacistsSerializer(profile, many=False)                            
                            return Response(serialised_profile.data, status=status.HTTP_200_OK)
                        else:
                            return Response('Invalid login credentials', status=statusBadRequest)
                    except Pharmacists.DoesNotExist:
                        try:
                            profile = Nurses.objects.get(username=username)
                            if(check_password(password, profile.password) == True):
                                now = getTimeNow()
                                payload = {'username': username, 'loggedinAt': now.strftime("%m/%d/%Y, %H:%M:%S")}
                                profile.token=encode_value(payload)                                                    
                                serialised_profile = PharmacistsSerializer(profile, many=False)                                
                                return Response(serialised_profile.data, status=status.HTTP_200_OK)
                            else:
                                return Response('Invalid login credentials', status=statusBadRequest)
                        except Nurses.DoesNotExist:
                            return Response('Username not found. Enter a valid username.', status=statusNotFound)
        else:
            return Response("Invalid login credentials. Make sure you filled in everything in the form", status=statusBadRequest)
    except:
        logger.error(traceback.format_exc())
        return Response("An error occured while authenticating you", status=statusBadRequest)    

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_patients(request):
    try:        
        listData = Patients.objects        
        for item in listData:            
            item["name"]=decrypt_value(item["name"])            
            item["email"]=decrypt_value(item["email"])
            item["phone_no"]=decrypt_value(item["phone_no"])
            item["date_of_birth"]=decrypt_value(item["date_of_birth"])
        serialized_listData = PatientsSerializer(listData, many=True)                                
        return Response(serialized_listData.data, status=status.HTTP_200_OK)
    except:
        logger.error(traceback.format_exc())
        return Response("An error occured while fetching all patients", status=statusBadRequest)    

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_doctors(request):
    try:
        listData = Doctors.objects
        for item in listData:            
            item["name"]=decrypt_value(item["name"])            
            item["email"]=decrypt_value(item["email"])
            item["phone_no"]=decrypt_value(item["phone_no"])
            item["date_of_birth"]=decrypt_value(item["date_of_birth"])
        serialized_listData = DoctorsSerializer(listData, many=True)                                
        return Response(serialized_listData.data, status=status.HTTP_200_OK)
    except:
        # logger.error(traceback.format_exc())
        return Response("An error occured while fetching all doctors", status=statusBadRequest)    

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_pharmacists(request):
    try:
        listData = Pharmacists.objects
        for item in listData:            
            item["name"]=decrypt_value(item["name"])            
            item["email"]=decrypt_value(item["email"])
            item["phone_no"]=decrypt_value(item["phone_no"])
            item["date_of_birth"]=decrypt_value(item["date_of_birth"])
        serialized_listData = PharmacistsSerializer(listData, many=True)                                
        return Response(serialized_listData.data, status=status.HTTP_200_OK)
    except:
        # logger.error(traceback.format_exc())
        return Response("An error occured while fetching all Pharmacists", status=statusBadRequest)    

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_nurses(request):
    try:
        listData = Nurses.objects
        for item in listData:            
            item["name"]=decrypt_value(item["name"])            
            item["email"]=decrypt_value(item["email"])
            item["phone_no"]=decrypt_value(item["phone_no"])
            item["date_of_birth"]=decrypt_value(item["date_of_birth"])
        serialized_listData = NursesSerializer(listData, many=True)                                
        return Response(serialized_listData.data, status=status.HTTP_200_OK)
    except:
        # logger.error(traceback.format_exc())
        return Response("An error occured while fetching all Nurses", status=statusBadRequest)    

@api_view(['GET'])
@permission_classes([isAuthorized])
def get_revenue(request):
    try:
        listData = Payments.objects
        total=0
        for payment in listData:
            total+=payment.amount_paid                            
        return Response(total, status=status.HTTP_200_OK)
    except:
        # logger.error(traceback.format_exc())
        return Response("An error occured while fetching all Nurses", status=statusBadRequest)     
        
@api_view(['POST'])
@permission_classes([isAuthorized])
def update_user(request):
    data = json.loads(request.body)
    try:        
        name=encrypt_value(data["name"])
        email=encrypt_value(data["email"])
        phone_no=encrypt_value(data["phone_no"])
        user_type=data["user_type"]
        user_id=data["id"]

        gender=None
        status=None
        date_of_birth=None
        fee=None
        specialization=None        

        if user_type=="doctor" or user_type=="nurse" or user_type=="pharmacist":
            gender=data["gender"]
            status=data["status"]
            date_of_birth=encrypt_value(data["date_of_birth"])            

        if user_type=="doctor" or user_type=="nurse":            
            specialization=data["specialization"]

        if user_type=="doctor":
            fee=data["fee"]                                        
                   
        if user_type=="doctor":
            Doctors.objects.filter(id=user_id).update(                                
                name=name,
                email=email,
                phone_no=phone_no,
                gender=gender,
                specialization=specialization,
                status=status,
                fee=fee,
                date_of_birth=date_of_birth,                
            )                    
        elif user_type=="nurse":
            Nurses.objects.filter(id=user_id).update(                                                
                name=name,
                email=email,
                phone_no=phone_no,
                gender=gender,
                specialization=specialization,
                status=status,                            
                date_of_birth=date_of_birth
            )   
        elif user_type=="pharmacist":
            Pharmacists.objects.filter(id=user_id).update(  
                name=name,
                email=email,
                phone_no=phone_no,
                gender=gender,                            
                status=status,                            
                date_of_birth=date_of_birth,
            )                                                    
        return Response('Successfully created an account for the new '+user_type.title()+' account', status=statusCreated)        
    except:
        logger.error(traceback.format_exc())
        return Response('An error occured while creating the new account', status=statusBadRequest)    
    
   
@api_view(['DELETE'])
@permission_classes([isAuthorized])
def delete_user(request,user_type,user_id):    
    try:               
        if user_type=="doctor":            
            Doctors.objects(id=user_id).delete()
        elif user_type=="nurse":
            Nurses.objects(id=user_id).delete()
        elif user_type=="pharmacist":            
            Pharmacists.objects(id=user_id).delete()                                                                           
        return Response('Successfully delete the account', status=statusCreated)        
    except:
        logger.error(traceback.format_exc())
        return Response('An error occured while deleting that account', status=statusBadRequest)     