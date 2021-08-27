from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('productSold', views.rest_api_view)

urlpatterns = [
    path('', include(router.urls)),
]
