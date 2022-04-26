from django.core import serializers
import json
from django.forms import ValidationError
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.request import Request
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import Group
from quickstart.models import Profile, Transactions, Plan, Profit, Referral
from rest_framework import viewsets, permissions
from quickstart.serializers import UserSerializer, ProfileSerializer, TransactionsSerializer,PlanSerializer, ProfileSerializer, ReferralSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .filters import TransactionsFilter
from rest_framework.authtoken.models import Token
from cryptocurrency_payment.models import CryptoCurrencyPayment, create_new_payment
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.core.serializers import serialize
from .myutils import generate_ref_code
from .models import MyUser
# User = get_user_model()

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
            'plans': 'links/plans/',
            'specific-plan':'links/plans/id/',
          	'all-users': 'links/users/',
        	'specific-user': 'links/users/id/',
          	'create-user': 'links/users/<ur posted data>/',
          	'all-transactions': '/transactions/',
            'search-transactions': 'transactions/?user=1&type=deposit&status=Paid/',
            'create-transaction': '/transactions/create/<ur posted data>/'

        }

	return Response(api_urls)

@api_view(['GET'])
def transactDetails(request):
    # for user in User.objects.all():
    #     Token.objects.get_or_create(user=user)
    """You can filter by 'user', 'type', 'status', 'sent', 'received'
      where status in "New", "Paid","Cancelled", "Processing".
      where type in 'deposit', 'withdraw'
      where sent/recieved in True or False.

    Keyword arguments: 
    argument -- ?user=1&type=deposit&status='Paid'
    Return: A list of dictionary objects containing the specific user transaction history
    allDeposit contains the total amount of deposits made by a user.
    allWithdraw does the same for amount withdrawn by a user.
    """
    queryset = Transactions.objects.all()
    filterset = TransactionsFilter(request.GET, queryset=queryset)
    if filterset.is_valid():
        queryset = filterset.qs
    serializer = TransactionsSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def create_myuser(request):
    profile_data = request.data.get('profile')
    first_name = request.data.get('first_name'),
    username = request.data.get('username'),
    last_name = request.data.get('last_name'),
    email = request.data.get('email')
    # user = User
    if MyUser.objects.filter(username=username).exists() or MyUser.objects.filter(email=email).exists():
        data = {"Message":"User already exists"}
    else: 
        try:
            user = MyUser.objects.create(
                first_name=request.data.get('first_name'),
                username=request.data.get('username'),
                last_name=request.data.get('last_name'),
                email=request.data.get('email')
            )
            user.set_password(request.data.get('password'))

            # Check of a ref code was sent
            code = profile_data.get('ref_code', None)
            if code != None:
                ref_by = Profile.objects.get(ref_code=code).user
                profile = Profile.objects.create(
                    user=user,
                    recomended_by=ref_by,
                    phone_number=profile_data['phone_number'],
                    ref_code=generate_ref_code()
                )
                profile.save()
                #CREATE THE USER WITHOUT THE REF CODE
            else:
                profile = Profile.objects.create(
                    user=user,
                    phone_number=profile_data['phone_number'],
                    ref_code=generate_ref_code()
                )
                profile.save()
                
            token = Token.objects.get_or_create(user=user)
            profile = {
                'ref_code':profile.ref_code,
                'phone_number':profile.phone_number
            }


            #REFEREl ND PROFITS PROFITS
            referred = Referral.objects.create(invitee=user)

            profit = Profit.objects.create(user=user)
            
            referred.save()
            user.save()
            profit.save()

            data = {'id':user.id, 'first_name':user.first_name, 'last_name':user.last_name, 'password':user.password,
            'email':user.email, 'profile':profile}
            # serializer = UserSerializer(data=data)
            # if serializer.is_valid():
            #     serializer.save()
            return Response(data)
        except Exception as e:
            print(e)
            return Response({'message':'An error occured while saving data'})

        


@api_view(['POST'])
def transactCreate(request):
    """Create a post request with the amount of investment and the id for the plan and the user

    Keyword arguments:
    argument --int: amount, plan id, user id
    Return: a link to complete payment process.
    """

    amount = request.data.get('amount')
    user_id = request.data.get('user_id')
    plan_id = request.data.get('plan_id')
    type = request.data.get('type')

    user = MyUser.objects.get(id=user_id)
    plan = Plan.objects.get(id=plan_id)

    payment = create_new_payment(crypto='BITCOIN',  # Cryptocurrency from your backend settings
                                 fiat_amount=amount,  # Amount of actual item in fiat
                                 fiat_currency='USD',  # Fiat currency used to convert to crypto amount
                                 payment_title=str(" Investment made  By " + \
                                                    user.username),  # Title associated with payment
                                 # Description associated with payment
                                 payment_description=f"{user.first_name} - {user.last_name} investment {plan.title}",
                                 # Generic linked object for this payment -> crypto_payments = GenericRelation(CryptoCurrencyPayment)
                                 related_object=None,
                                 user=user,  # User of this payment for non-anonymous payment
                                 parent_payment=None,  # Obvious
                                 address_index=None,  # Use a particular address index for this payment
                                 reuse_address=None)  # Used previously paid address for this payment
    pid = payment.id
    # print(payment)
    # 'crypto_payment_detail'
    transact = Transactions.objects.create(user=user, plan=plan, amount=amount, status=payment.status, tid=pid)
    transact.save()

    serializer = TransactionsSerializer(data={'user':user_id, 'plan':plan_id, 'amount':amount, 'status':payment.status, 'tid':pid})
    if serializer.is_valid():
        serializer.save()

    url = reverse('cryptocurrency_payment:crypto_payment_detail', kwargs={"pk": pid})
    data = serializer.data
    data['url'] = f"http://localhost:8000{url}"
    return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MyUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def user_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')

@api_view(["POST"])
def login_user(request):

    data = {}
    reqBody = json.loads(request.body)
    email1 = reqBody['Email_Address']
     
    print(email1)
    password = reqBody['password']
    try:

        Account = MyUser.objects.get(email=email1)
    except BaseException as e:
        return Response({"message": "user doesnt exist"})
        raise ValidationError({"400": f'{str(e)}'})

    token = Token.objects.get_or_create(user=Account)[0].key
    print(token)
    if not check_password(password, Account.password):
        return Response({"message":"Incorrect Login credentials"})
        # raise ValidationError({"message": "Incorrect Login credentials"})

    if Account:
        if Account.is_active:
            print(request.user)
            login(request, Account)
            data["message"] = "user logged in"
            data["user"] = Account.id
            data["email_address"] = Account.email

            Res = {"data": data, "token": token}

            return Response(Res)

        else:
            return Response({"message": 'Account not active'})

    else:
        return Response({"message": 'Account doesnt exist'})






class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Plan.objects.all().order_by('-id')
    serializer_class = PlanSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('-id')
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user',]
    # permission_classes = [permissions.IsAuthenticated]


