from django.urls import path,include
from farmers import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('/register', views.register, name='register'),
   path('/login', views.login, name='login'),
   path('/', views.home, name='home')
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)