from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    UserProfileList,
    UserProfileDetail,
    request_password_reset,
    password_reset_confirm,
    whoami,
    change_user_role,
    UserListAdminView,  # Added missing import
    delete_user,  # Added missing import
    MyUserProfileView,  # Added missing import
)


urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    path('api/userprofiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('api/userprofiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('api/users/<int:pk>/delete/', delete_user, name='user-delete'), # Changed path for clarity
    path('api/whoami/', whoami, name='whoami'),
    path('api/changerole/<int:user_id>/', change_user_role, name='change_user_role'),
    path('api/admin/users/', UserListAdminView.as_view(), name='admin-user-list'),
    path('api/myprofile/', MyUserProfileView.as_view(), name='myprofile'),



    path('api/password-reset/', request_password_reset, name='password-reset'),
    path('api/password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password-reset-confirm'),
]