
from datetime import datetime
from quickstart.models import Profit, Transactions


def confirm_deposit():
    for transaction in Transactions.objects.filter(recieved=False):
        time = transaction.time
        tot_time = time - datetime.datetime.now()
        mins = tot_time.seconds() / 60
        if mins > 5:
            transaction.sent = True
            transaction.save()


def confirm_withdraw():
    for transaction in Transactions.objects.filter(sent=False):
        time = transaction.time
        tot_time = time - datetime.datetime.now()
        mins = tot_time.seconds / 60
        if mins > 5:
            transaction.sent = True
            transaction.save()

def get_profit():
    profit = Profit.objects.all()
    total_deposit = Transactions.objects.filter(user=profit.user)[0].get_allDeposit() if Transactions.objects.filter(user=profit.user).exist() else 0
    profit.amount += round(total_deposit * 0.20, 2)
    profit.save()


def withdraw_status():
    for profit in Profit.objects.all():
        if profit.amount > 0:
            time  = profit.time
            if time - datetime.datetime.now().days >= 14:
                profit.can_withdraw = True
                profit.save()

            