from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile, Transactions, Plan, Profit, Referral


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'

class TransactionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transactions
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'

class PlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plan
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'

class ProfitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profit
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'

class ReferralSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Referral
        # fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups']
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
