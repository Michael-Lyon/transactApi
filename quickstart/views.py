from django.shortcuts import render
from django.contrib.auth.models import User, Group
from quickstart.models import Profile, Transactions, Plan, Profit, Referral
from rest_framework import viewsets, permissions
from quickstart.serializers import UserSerializer, GroupSerializer, ProfileSerializer, TransactionsSerializer,PlanSerializer, ProfileSerializer, ReferralSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited. just for nothing
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('-id')
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]

class TransactionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transactions.objects.all().order_by('-id')
    serializer_class = TransactionsSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Plan.objects.all().order_by('-id')
    serializer_class = PlanSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProfitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profit.objects.all().order_by('-id')
    serializer_class = ProfileSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ReferralViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Referral.objects.all().order_by('-id')
    serializer_class = ReferralSerializer
    # permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]
