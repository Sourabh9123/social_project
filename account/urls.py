from django.urls import path 
from account.views import LogInview, SignUpView



urlpatterns = [
    path("login/", LogInview.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    

]