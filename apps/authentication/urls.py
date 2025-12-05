from django.urls import path

from .views import UserRegisterView, UserLogoutView, UserLoginView

app_name = 'apps.authentication'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(next_page='/login/'), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),

]