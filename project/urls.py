from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from items.views import NotesListAPI, home_view
from django.conf import settings
from accounts.views import CreateUserView, ChangePasswordAPIView, LoginView, RegisterView, RequestChangePasswordAPI


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('api/notes/', NotesListAPI.as_view()), # List notes endpoint
    path('api/token/', TokenObtainPairView.as_view()), # Get access token endpoint 
    path('api/token/refresh/', TokenRefreshView.as_view()), # Get refresh token endpoint
    path('api/create-user/', CreateUserView.as_view()), # Create new user ( Registeration ) endpoint

    # Change password for user endpoint
    path('api/change-password/', ChangePasswordAPIView.as_view(), name="change_password"),

    # Forget password / Make temporary password for user endpoint
    path('api/forget-password/', RequestChangePasswordAPI.as_view(), name="request_change_password")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)