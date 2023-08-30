from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friends/<uuid:pk>/', api.friends, name='friends'),
    path('editprofile/', api.edit_profile, name='edit_profile'),
    path('editpassword/', api.edit_password, name='edit_password'),
    path('friends/<uuid:pk>/request/', api.send_friend_request,
         name='send_friend_request'),
    path('friends/suggested/', api.my_friend_suggestions,
         name='my_friend_suggestions'),
    path('friends/<uuid:pk>/<str:status>/',
         api.handle_request, name='handle_request'),
]
