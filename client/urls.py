from django.urls import path
from .views.activeuser import activeuser, users, deactiveuser
from .views.status import status
from .views.courses import courses
from .views.index import index
from .views.login import Login
from .views.logout import Logout
from .views.profile import profile
from .views.setting import settings, configs
from .views.verify import verify
from .views.changepassword import changepassword
from .views.installation import admin, admininstall, adminremove, createuser
app_name = 'client'
urlpatterns = [
    path('', index, name="index"),

    path('profile/', profile, name="profile"),
    path('profile/edit/', profile, {'action': 'edit'}, name="profile-edit"),
    path('profile/password/', changepassword, name="password"),

    path('setting/', settings, name="setting"),
    path('setting/edit/', settings, {'action': 'edit'}, name="setting_edit"),
    path('setting/<str:domain>', configs, name="configs"),

    path('courses/', courses, name="courses"),

    path('login/', Login, name="login"),
    path('verify/', verify, name="verify"),
    path('logout/', Logout, name="logout"),

    path('status/', status, name="status"),

    path('users/', users, name="users"),
    path('users/<int:id>/active', activeuser, name="activeuser"),
    path('users/<int:id>/deactive', deactiveuser, name="deactiveuser"),

    path('admin/', admin, name="admin"),
    path('admin/<int:id>/', admin, name="admin"),
    path('admin/<int:id>/install/', admininstall, name="admininstall"),
    path('admin/<int:id>/remove/', adminremove, name="adminremove"),
    path('admin/<str:domain>/createuser/', createuser, name="createuser"),
]
