from django.urls import path,include
from customers import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.home, name='customerhome'),
    path('login/',views.login,name='customerlogin'),
    path('logout/',views.logout, name='logout'),
    path('register/',views.register,name='customerregister'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('userprofile/createprofile',views.createprofile,name='customerprofile'),
    path('userprofile/updateprofile', views.updateprofile,name='updateprofile'),
    path('track', views.track, name='track' ),
    path('customerproducts/',views.customerproducts, name='customerproducts'),
    path('updatecart', views.updateCart, name = 'updatecart'),
    path('cart', views.cart, name = 'cart'),
    path('productSearch', views.productSearch, name = 'productSearch'),
    path('updatequantity', views.updateQuantity, name = 'updatequantity'),
    path('productdetail/<str:slug>/', views.productDetail, name = 'productDetail'),
    path('payment/',views.payment,name='payment')
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)