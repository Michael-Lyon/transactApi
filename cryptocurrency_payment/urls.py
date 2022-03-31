# -*- coding: utf-8 -*-
from django.urls import re_path
from cryptocurrency_payment import views

app_name = 'cryptocurrency_payment'
urlpatterns = [

    re_path(
        "payment/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$",
        views.CryptoPaymentDetailView.as_view(),
        name='crypto_payment_detail',
    ),

]
