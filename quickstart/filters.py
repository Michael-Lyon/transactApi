import django_filters
from .models import Transactions

class TransactionsFilter(django_filters.FilterSet):
    class Meta:
        model = Transactions
        fields = ['user', 'type', 'tid', 'sent', 'recieved']
