from django.urls import path,include
from .views import users as user_view
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("users",user_view.UserApiView,basename="user")

urlpatterns = [
    path("",include(router.urls)),
    path("accounts/login/",user_view.UserLoginApiView.as_view()),
    path("accounts/register/",user_view.UserRegisterApiView.as_view()),
    path("accounts/refresh_token/",user_view.RefreshTokenApiView.as_view()),
    path("accounts/logout/",user_view.UserLogoutApiView.as_view()),
    path("accounts/me/profile/",user_view.MyAccountApiView.as_view()),
    path("accounts/my-address/",user_view.AddressApiView.as_view()),
    path("accounts/change-password/",user_view.ChangePasswordApi.as_view()),

    # path("my-profile/",MyAccountApiView.as_view()),
    
]
