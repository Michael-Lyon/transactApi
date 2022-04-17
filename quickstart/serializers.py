from django.utils.timezone import now
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, Transactions, Plan, Profit, Referral
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone_number', 'ref_code']
        # fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'username', 'last_name', 'password', 'email', 'days_since_joined', 'profile', )

    def create(self, validated_data):
        # create user
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        user.save()
        token = Token.objects.get_or_create(user=user)
        profile_data = validated_data.pop('profile')
        profile = Profile.objects.create(
            user=user,
            phone_number=profile_data['phone_number'],
        )
        profile.save()
        return user

    def get_days_since_joined(self, obj):
        print(obj)
        return (now() - obj.date_joined).days


class TransactionsSerializer(serializers.ModelSerializer):
    """sumary_line
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    allDeposit = serializers.SerializerMethodField()
    allWithdraw = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Transactions
        fields = ['user', 'plan', 'type', 'amount', 'time', 'tid', 'status','wallest_add', 'allDeposit', 'allWithdraw', 'profit']

    def get_allDeposit(self, obj):
        # print(obj)
        return obj.get_allDeposit()

    def get_profit(self, obj):
        return obj.user.userprofit.amouont if Profit.objects.filter(user=obj.user).exists() else 0
    def get_allWithdraw(self, obj):
        # print(obj)
        return obj.get_allWithdraws()

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'

class ProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profit
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
