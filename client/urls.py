from django.urls import path
from .views import *

app_name = 'client'
urlpatterns = [
    path('', index, name="index"),

    path('profile/', profile, name="profile"),
    # path('profile/edit/', profile, {'action': 'edit'}, name="profile-edit"),
    path('profile/edit/<int:user_id>/', profile_edit, name="profile_edit"),
    path('profile/edit/<int:user_id>/', profile_edit, name="profile_update"),
    path('profile/password/', changepassword, name="password"),

    path('setting/', user_settings, name="setting"),
    path('setting/edit/', user_settings, {'action': 'edit'}, name="setting_edit"),
    path('setting/<str:domain>/', configs, name="configs"),
    path('setting/<str:domain>/<path:path>', static_files, name="static_files"),

    path('login/', login, name="login"),
    path('verify/<str:user_cellphone>/', verify, name="verify_get"),
    path('logout/', Logout, name="logout"),

    path('status/', status, name="status"),

    path('users/', users, name="users"),
    path('users/<int:user_id>/active', activate_user, name="activeuser"),
    path('users/<int:user_id>/deactive', deactivate_user, name="deactiveuser"),
    path('plus_update_pass/', plus_update_pass, name="plus_update_pass"),

    path('admin/', admin, name="admin"),
    path('admin/<int:id>/', admin, name="admin"),
    path('admin/<int:id>/install/', admininstall, name="admininstall"),
    path('admin/<int:id>/install-sites/', install_sites, name="install-sites"),
    path('admin/<int:id>/remove/', adminremove, name="adminremove"),
    path('admin/<int:id>/siteuser/', check_or_createuser, name="siteuser"),
    path('admin/<str:id>/<str:user>/resetpassword/', resetpassword, name="resetpassword"),

    path('version/', verion, name="view_verion"),
    path('version/edit/<int:id>/', edit_verion, name="edit_verion"),
    path('version/create/', create_verion, name="create_verion"),
    path('version/active/<int:id>/', edit_verion, {'action' : 'active'}, name="active_verion"),
    path('version/deactive/<int:id>/', edit_verion, {'action' : 'deactive'}, name="deactive_verion"),
]
