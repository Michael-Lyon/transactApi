from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from quickstart import views
from rest_framework.authtoken import views as v
from cryptocurrency_payment import urls as cryptocurrency_payment_urls
from django.conf.urls.static import static
from tutorial.settings import STATIC_ROOT, STATIC_URL

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'profiles', views.ProfileViewSet)
# router.register(r'transactions', views.TransactionsViewSet)
router.register(r'plans', views.PlanViewSet)
# router.register(r'referral', views.ReferralViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('links/users/create/', views.create_myuser),
    path('admin/', admin.site.urls),
    path('links/', include(router.urls)),
    path('', views.apiOverview),
    path('transactions/create/', views.transactCreate),
    path('transactions/', views.transactDetails),
    path('login/', views.login_user),
    path('logout/', views.user_logout),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', v.obtain_auth_token),
    re_path(r'^', include(cryptocurrency_payment_urls)),
] + static(STATIC_URL, document_root=STATIC_ROOT)
