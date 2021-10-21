from django.urls import path

from .views.courses import courses
from .views.index import index
from .views.login import Login
from .views.profile import profile
from .views.setting import settings
from .views.signup import signup
from .views.verify import verify
from .views.changepassword import changepassword

app_name = 'client'



urlpatterns = [
    path('', index, name="index"),
    path('profile/', profile, name="profile"),
    path('profile/password/', changepassword, name="password"),
    path('setting/', settings, name="setting"),
    path('courses/', courses, name="courses"),
    path('login/', Login, name="login"),
    path('signup/', signup, name="signup"),
    path('verify/', verify, name="verify"),
]
