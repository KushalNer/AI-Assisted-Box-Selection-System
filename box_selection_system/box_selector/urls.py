from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, BoxViewSet

router = DefaultRouter()
router.register('product',ProductViewSet,basename='products')
router.register('box',BoxViewSet,basename='boxes')



urlpatterns = [
    path('api/',include(router.urls)),

]
