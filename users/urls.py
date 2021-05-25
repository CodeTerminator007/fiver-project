from .views import UserActivationView
from django.conf.urls import url , include
from django.urls import path
from products.views import CartItemViewSet ,CartItemupdateViewSet


urlpatterns = [
    url(r'^users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    path('cart/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart/<str:pk>',CartItemupdateViewSet.as_view({'delete':'destroy','put': 'update','patch': 'partial_update',}))

]