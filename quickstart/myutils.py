from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

import uuid 
import random
import string
User = get_user_model()

def generate_ref_code():
    letters = string.ascii_lowercase
    code= ''.join(random.choice(letters) for i in range(6))
    return code



# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)
