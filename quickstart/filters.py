# from cProfile import Profile
import django_filters
from .models import Transactions, Profile

class TransactionsFilter(django_filters.FilterSet):
    class Meta:
        model = Transactions
        fields = ['user', 'type', 'tid', 'sent', 'recieved']

class ProfileFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['user']
