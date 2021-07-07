from django.contrib.auth.decorators import login_required
from django.urls import path, reverse
from account.views import AccountIndexView, logout_view, login_view, signup

LOGIN_REDIRECT_URL = "/account/login"
app_name = 'account'
urlpatterns = [
    path('', login_required(AccountIndexView.as_view(), login_url=LOGIN_REDIRECT_URL), name='index'),
    path('logout', logout_view, name='logout'),
    path('login', login_view, name='login'),
    path('signup', signup, name='signup'),
]
