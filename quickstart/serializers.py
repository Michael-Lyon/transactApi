from hashid_field import Hashid
from django.utils.timezone import now
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import MyUser, Profile, Transactions, Plan, Profit, Referral
from rest_framework.authtoken.models import Token
from django.conf import settings
from hashid_field import Hashid
from hashid_field.rest import HashidSerializerCharField

User = settings.AUTH_USER_MODEL
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = ['phone_number', 'ref_code']
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    profile = ProfileSerializer(required=True)
    days_since_joined = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()
    class Meta:
        model = MyUser
        # fields = '__all__'
        fields = ('id','first_name', 'username', 'last_name', 'password', 'email', 'days_since_joined','referrals', 'profile')


    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days
    
    def get_id(self, obj):
        id = obj.id
        return id

    def get_referrals(self, obj):
        return Profile.objects.get(user=obj).get_recommened_profiles() if Profile.objects.filter(user=obj).exists() else "No referrals"
        
        

class TransactionsSerializer(serializers.ModelSerializer):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """


    allDeposit = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    allWithdraw = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    withdraw_status = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()


    # user = serializers.PrimaryKeyRelatedField(
    #     pk_field=HashidSerializerCharField(source_field='quickstart.MyUser.id'),
    #     queryset=MyUser.objects.all())
    class Meta:
        model = Transactions
        fields = ('id', 'user', 'plan', 'type', 'amount', 'time', 'tid', 'status',
                  'wallest_add', 'allDeposit', 'allWithdraw', 'profit', 'withdraw_status')

    def get_allDeposit(self, obj):
        # print(obj)
        return obj.get_allDeposit()

    def get_profit(self, obj):
        return obj.user.userprofit.get().amount if Profit.objects.filter(user=obj.user).exists() else 0
    
    def get_withdraw_status(self, obj):
        return obj.user.userprofit.get().can_withdraw if Profit.objects.filter(user=obj.user).exists() else 0
    
    
    def get_allWithdraw(self, obj):
        # print(obj)
        return obj.get_allWithdraws()

    def get_user(self, obj):
        id = obj.user.id
        return id


    def get_id(self, obj):
        id = obj.id
        # s = id.hashid
        return id

class PlanSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    class Meta:
        model = Plan
        fields = ['id', 'title', 'max_price', 'min_price', 'rate', 'description1']
        # fields = '__all__'
    
    def get_id(self, obj):
        id = obj.id
        return id

class ProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profit
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'
    
    # def get_id(self, obj):
    #     id = obj.id
    #     return id.hashid

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

# {
#     "id": "71q6wRe",
#     "title": "Agency Plan",
#     "max_price": None,
#     "min_price": 10000.0,
#     "rate": 17.0,
#     "description1": "Agency Plan"
# },
# {
#     "id": "EaRpXRK",
#     "title": "Assembled Plan",
#     "max_price": 4999.0,
#     "min_price": 3000.0,
#     "rate": 19.0,
#     "description1": "Assembled"
# },
# {
#     "id": "lpnO3ny",
#     "title": "Promo Plan",
#     "max_price": 5000.0,
#     "min_price": 3000.0,
#     "rate": 12.0,
#     "description1": "Promo"
# },
# {
#     "id": "l8qM0nL",
#     "title": "Administative Plan",
#     "max_price": 9999.0,
#     "min_price": 4000.0,
#     "rate": 19.0,
#     "description1": "Administrative"
# },
# {
#     "id": "lpqvmnb",
#     "title": "Diamond Plan",
#     "max_price": 3999.0,
#     "min_price": 1000.0,
#     "rate": 10.0,
#     "description1": "Diamond Plan"
# },
# {
#     "id": "73Z9yZp",
#     "title": "Beginner's Plan",
#     "max_price": 999.0,
#     "min_price": 50.0,
#     "rate": 17.0,
#     "description1": "A simple plan"
# },
# {
#     "id": "5JnK0qB",
#     "title": "Demo Plan",
#     "max_price": 300000.0,
#     "min_price": 200.0,
#     "rate": 12.0,
#     "description1": "Just a demo"
# }
