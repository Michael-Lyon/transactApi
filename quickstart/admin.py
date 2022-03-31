from django.contrib import admin

from .models import Transactions
# Register your models here.
# admin.site.register(Plan)
# admin.site.register(SelectPlan)
# admin.site.register(Referral)
# admin.site.register(Profit)
# admin.site.register(Personal_Tweak)


def withdraw_sent(modeladmin, request, queryset):
    # print(queryset)
    for query in queryset:
        amount = query.amount
        user = query.user
        pro = user.userprofit.get()
        print(pro.amount)
        pro.amount -= amount
        pro.can_withdraw = False
        pro.save()
    queryset.update(sent=True)
    queryset.update(status="Completed")



withdraw_sent.short_description = "All pending withdrawals sent"


@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'type',
        'sent',
        'time',
        'recieved'
    ]

    list_filter = [
        'type',
        'sent',
        'recieved'
    ]

    search_fields = [
        'user',
        'tid',
    ]

    actions = [
        withdraw_sent
    ]
