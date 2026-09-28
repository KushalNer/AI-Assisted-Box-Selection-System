from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Product, Box
from .serializers import ProductSerializer, BoxSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
