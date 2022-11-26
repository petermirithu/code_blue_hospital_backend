from .models import *

def checkUsernameTaken(username):
    try:
        found = Administrators.objects.get(username=username)
        return True
    except Administrators.DoesNotExist:
        try:
            found = Doctors.objects.get(username=username)
            return True
        except Doctors.DoesNotExist:
            try:
                found = Nurses.objects.get(username=username)
                return True
            except Nurses.DoesNotExist:
                try:
                    found = Pharmacists.objects.get(username=username)
                    return True
                except Pharmacists.DoesNotExist:
                     return False
