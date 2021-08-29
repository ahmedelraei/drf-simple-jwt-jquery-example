from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from items.views import NotesListAPI, home_view
from django.conf import settings
from accounts.views import CreateUserView, ChangePasswordAPIView, LoginView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('api/notes/', NotesListAPI.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/create-user/', CreateUserView.as_view()),
    path('api/change-password/', ChangePasswordAPIView.as_view())
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)