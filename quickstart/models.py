from .myutils import generate_ref_code
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import reverse
from django.db.models import Sum
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models.fields import DateTimeField
from django.db import models
# from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser
from hashid_field import HashidAutoField

class MyUser(AbstractUser):
    id = HashidAutoField(primary_key=True)
    

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    ref_code = models.CharField(max_length=15)
    recomended_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    signup_confirmation = models.BooleanField(default=False)
    dob = models.CharField(max_length=300, blank=True, null=True,)
    permanent_address = models.CharField(max_length=400, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    present_address = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    wallest_add = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        my_recs = []
        for profile in qs:
            try:
                if profile.recomended_by == self.user:
                    my_recs.append(profile.user.username)
            except Exception as e:
                pass
        return my_recs
# User = get_user_model()

LABEL_CHOICES = (
    ('one', 'One 1'),
    ('two', 'Two 2'),
    ('three', 'Three 3'),
    ('four', 'Four 4'),
    ('five', 'Five 5'),
)


class Plan(models.Model):
    id = HashidAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    label = models.CharField(choices=LABEL_CHOICES, max_length=10)
    max_price = models.FloatField(null=True, blank=True)
    min_price = models.FloatField()
    slug = models.SlugField()
    rate = models.FloatField()
    description1 = models.CharField(max_length=30)
    description2 = models.CharField(max_length=30, null=True, blank=True)
    description3 = models.CharField(max_length=30, null=True, blank=True)
    description4 = models.CharField(max_length=30, null=True, blank=True)
    description5 = models.CharField(max_length=30, null=True, blank=True)
    description6 = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})


class Transactions(models.Model):
    id = HashidAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, blank=True, null=True, default="deposit")
    status = models.CharField(max_length=20, blank=True, null=True, default="Processing")
    amount = models.FloatField(default=0)
    wallest_add = models.CharField(max_length=200, blank=True, null=True)
    sent = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now=True)
    tid = models.CharField(max_length=250)
    

    def __str__(self):
        return f"{self.user} made {self.type} of {self.amount}"

    def get_allDeposit(self):
        # who = kwargs.get('who')
        total = Transactions.objects.filter(user=self.user, type="deposit", recieved=True).aggregate(Sum('amount'))
        return total['amount__sum'] if total['amount__sum'] is not None else 0

    def get_allWithdraws(self):
        # who = kwargs.get('who')
        total = Transactions.objects.filter(user=self.user, type="withdraw", sent=True).aggregate(Sum('amount'))
        return total['amount__sum'] if total['amount__sum'] is not None else 0

    # def save(self, *args, **kwargs):
    #     self.tid = generate_ref_code()
    #     super().save(*args, **kwargs)


class Referral(models.Model):
    # id = HashidAutoField(primary_key=True)
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.invitee}'


class Profit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userprofit")
    amount = models.FloatField(default=0)
    time = models.DateTimeField(auto_now=True)
    can_withdraw = models.BooleanField(default=False)


class Personal_Tweak(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="geng")
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user.username} in in geng'
