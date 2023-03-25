from django.urls import path,include
from farmers import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('/farmerregister', views.farmerregister, name='farmerregister'),
   path('/farmerlogin', views.farmerlogin, name='farmerlogin'),
   path('/farmerhome', views.farmerhome, name='farmerhome'),
   path('/farmerlogout', views.farmerlogout, name='farmerlogout'),
   path('/farmerprofile', views.farmerprofile, name='farmerprofile'),
   path('/farmerproduct', views.farmerproduct, name='farmerproduct'),
   path('/farmerupload', views.farmerupload, name='farmerupload'),
   path('/createprofile', views.createprofile,name='createprofile'),
   path('/updateprofile', views.updateprofile, name='updateprofile'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)