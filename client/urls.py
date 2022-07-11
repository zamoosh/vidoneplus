from django.urls import path
from .views import *
from .api import *

app_name = 'client'
urlpatterns = [
    path('', dashboard, name='dashboard'),

    path('profile/', profile, name='profile'),
    path('profile/password/', changepassword, name="password"),
    path('user/edit/<int:user_id>/', user_edit, name='user_edit'),

    path('setting/', user_settings, name="setting"),
    path('setting/edit/', user_settings, {'action': 'edit'}, name="setting_edit"),

    path('setting/<str:domain>/<path:path>', static_files, name="static_files"),

    path('login/', login, name="login"),
    path('verify/<str:user_cellphone>/', verify, name="verify"),
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

    path('versions/', versions, name="versions"),
    path('versions/delete/<int:image_tag_id>/', version_delete, name="version_delete"),
    path('version/edit/<int:image_tag_id>/', version_edit, name='version_edit'),
    path('version/create/', version_create, name='version_create'),
    path('version/active/<int:id>/', edit_verion, {'action' : 'active'}, name="active_verion"),
    path('version/deactive/<int:id>/', edit_verion, {'action' : 'deactive'}, name="deactive_verion"),

    path('sites/', sites, name="sites"),

    # api
    path('api/select/theme/', api_select_theme, name='api_select_theme'),
    path('api/get/domain/config/<str:domain>/', api_get_domain_config, name='api_get_domain_donfig'),
    path('api/available/versions/', api_get_available_force_version, name='api_available_versions')
]
