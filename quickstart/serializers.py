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
        return obj.user.userprofit.amount if Profit.objects.filter(user=obj.user).exists() else 0
    
    def get_withdraw_status(self, obj):
        return obj.user.userprofit.can_withdraw if Profit.objects.filter(user=obj.user).exists() else 0
    
    
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
    class Meta:
        model = Plan
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'
    
    # def get_id(self, obj):
    #     # print(obj.my_id)
    #     id = obj.id
    #     # print(h)
    #     return id.hashid

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
