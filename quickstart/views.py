import json
from django.forms import ValidationError
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.request import Request
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User, Group
from quickstart.models import Profile, Transactions, Plan, Profit, Referral
from rest_framework import viewsets, permissions
from quickstart.serializers import UserSerializer, GroupSerializer, ProfileSerializer, TransactionsSerializer,PlanSerializer, ProfileSerializer, ReferralSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .filters import TransactionsFilter
from rest_framework.authtoken.models import Token
from cryptocurrency_payment.models import CryptoCurrencyPayment, create_new_payment
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password

User = get_user_model()


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

    user = User.objects.get(id=user_id)
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
    print(payment)
    'crypto_payment_detail'
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
    queryset = User.objects.all().order_by('-date_joined')
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

        Account = User.objects.get(email=email1)
    except BaseException as e:
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
            data["email_address"] = Account.email

            Res = {"data": data, "token": token}

            return Response(Res)

        else:
            return Response({"message": 'Account not active'})

    else:
        return Response({"message": 'Account doesnt exist'})




# class TransactionsViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Transactions.objects.all().order_by('-id')
#     serializer_class = TransactionsSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['type', 'user']

    # permission_classes = [permissions.IsAuthenticated]
    # @action(detail=True)

    # def list(self, request, user_id=None):
    #     if user_id is None:
    #         serializer = TransactionsSerializer(self.queryset, many=True, context={'request': request})
    #         return Response(serializer.data)
    #     if user_id:
    #         print("Heyyyy")
    #         print(user_id)
    #         user = User.objects.get(id=user_id)
    #         list = get_object_or_404(self.queryset, user=user)
    #         serializer = TransactionsSerializer(list)
    #         return Response(serializer.data)    

class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Plan.objects.all().order_by('-id')
    serializer_class = PlanSerializer
    # permission_classes = [permissions.IsAuthenticated]

# class ProfitViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Profit.objects.all().order_by('-id')
#     serializer_class = ProfileSerializer
#     # permission_classes = [permissions.IsAuthenticated]

# class ReferralViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Referral.objects.all().order_by('-id')
#     serializer_class = ReferralSerializer
#     # permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     # permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer

    # permission_classes = [permissions.IsAuthenticated]
