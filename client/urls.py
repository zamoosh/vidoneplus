from django.urls import path
from .views import *

app_name = 'client'
urlpatterns = [
    path('', index, name="index"),

    path('profile/', profile, name="profile"),
    path('profile/edit/', profile, {'action': 'edit'}, name="profile-edit"),
    path('profile/password/', changepassword, name="password"),

    path('setting/', user_settings, name="setting"),
    path('setting/edit/', user_settings, {'action': 'edit'}, name="setting_edit"),
    path('setting/<str:domain>/', configs, name="configs"),
    path('setting/<str:domain>/<path:path>', static_files, name="static_files"),

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
    path('admin/<int:id>/install-sites/', install_sites, name="install-sites"),
    path('admin/<int:id>/remove/', adminremove, name="adminremove"),
    path('admin/<int:id>/siteuser/', check_or_createuser, name="siteuser"),
    path('admin/<str:user>/resetpassword/', resetpassword, name="resetpassword"),
]
