import traceback
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.response import Response
from rest_framework import status
from .permissions import isAuthorized
from .models import *
from .enc_decryption import hash_password,check_password,encode_value
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
# @permission_classes([isAuthorized])
def register_user(request):
    data = json.loads(request.body)
    try:
        username = data['username']        
        password = data['password']
        name=data["name"]
        email=data["email"]
        phone_no=data["phone_no"]
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
            date_of_birth=data["date_of_birth"]  
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
        # logger.error(traceback.format_exc())
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
                    except:
                        return Response('Username not found. Enter a valid username.', status=statusNotFound)
        else:
            return Response("Invalid login credentials. Make sure you filled in everything in the form", status=statusBadRequest)
    except:
        # logger.error(traceback.format_exc())
        return Response("An error occured while authenticating you", status=statusBadRequest)    