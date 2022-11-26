from rest_framework import permissions
from datetime import datetime
from .enc_decryption import decode_value


class isAuthorized(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            token = request.headers["Authorization"].replace("Bearer ", "")            
            if(token):
                try:                    
                    value = decode_value(token) 
                    loggedIn = datetime.strptime(value['loggedinAt'], "%m/%d/%Y, %H:%M:%S")                    
                    now = datetime.now()                    
                    difference=now-loggedIn
                    hours=difference.total_seconds() / 3600                   
                    if(hours<(24*7)):
                        return True
                    else:
                        return False
                except:                    
                    return False
            else:                
                return False
        except:            
            return False