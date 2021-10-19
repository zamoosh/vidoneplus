from django.urls import path
from .views.login import Login
from .views.signup import signup
from .views.verify import verify

app_name = 'client'
urlpatterns = [
    path('login/', Login, name="login"),
    path('signup/', signup, name="signup"),
    path('verify/', verify, name="verify"),
]
