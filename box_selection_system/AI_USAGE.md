-- Which AI Tool Used --

I used ChatGPT for:
    - suggestions for model design 
    - box recommandation api design 
    - identify possible test cases

 -- Prompts Used --
    
- I am building a small Django-based ecommerce shipping box recommendation system.
 
- Create django models for Product and Box for this project. Include fields: Product — name, length, width, height, weight; Box — name, internal_length, internal_width, internal_height, max_weight, cost.
use suitable django field types for dimensions, weight, and cost, with basic validation.

- create  logic to recommend the most suitable shipping box for an order based on product dimensions and weight.

- update the box recommendation logic so that product length, width, and height  check with  box's corresponding internal dimensions without using sorted

- Create API for the box recommendation logic for multiple product

- Used model serializer and modelviewset

- create test cases for the box recommendation service covering all important valid, invalid, edge, and failure problem

- create  test cases for the box recommendation API endpoint covering all important valid, invalid, edge, and failure problem  class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="recommend"
    )
    def recommend(self, request):

        serializer = BoxRecommendationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data["product_ids"]

        products= Product.objects.filter(
            id__in=product_ids
        )

        if products.count() != len(set(product_ids)):
            return Response(
                {
                    "error": "One or more products were not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        box = recommend_box(products)

        if not box:
            return Response(
                {
                    "message": "No suitable box found."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "box": BoxSerializer(box).data
            },
            status=status.HTTP_200_OK
        )



-- AI Output Accepted --
1)
from django.core.validators import MinValueValidator
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(max_length=200)

    internal_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    internal_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    internal_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name

2)
from decimal import Decimal

from .models import Box


def can_product_fit_box(product, box):
    product_dimensions = sorted([
        product.length,
        product.width,
        product.height
    ])

    box_dimensions = sorted([
        box.internal_length,
        box.internal_width,
        box.internal_height
    ])

    return all(
        product_dim <= box_dim
        for product_dim, box_dim in zip(product_dimensions, box_dimensions)
    )


def recommend_box(products):
    """
    Recommend the lowest-cost box that can fit all products
    and support their combined weight.
    """

    products = list(products)

    if not products:
        return None

    total_weight = sum(
        (product.weight for product in products),
        Decimal("0")
    )

    suitable_boxes = []

    for box in Box.objects.all():

        # Check total weight
        if total_weight > box.max_weight:
            continue

        # Check whether every product fits inside the box
        if all(can_product_fit_box(product, box) for product in products):
            suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    # Recommend the lowest-cost suitable box
    return min(suitable_boxes, key=lambda box: box.cost)

3)
class BoxRecommendationSerializer(serializers.Serializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False
    )

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="recommend"
    )
    def recommend(self, request):

        serializer = BoxRecommendationSerializer(
            data=request.data
        )
    ts     serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data["product_ids"]

        produc= Product.objects.filter(
            id__in=product_ids
        )

        if products.count() != len(set(product_ids)):
            return Response(
                {
                    "error": "One or more products were not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        box = recommend_box(products)

        if not box:
            return Response(
                {
                    "message": "No suitable box found."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "box": BoxSerializer(box).data
            },
            status=status.HTTP_200_OK
        )
4)
- test_services.py file
- test_api.py file



-- output rejected or modified --
1) this rejected because its only for single product box recommend
from decimal import Decimal
from .models import Box


def can_product_fit_box(product, box):
    return (
        product.length <= box.internal_length
        and product.width <= box.internal_width
        and product.height <= box.internal_height
    )


def recommend_box(products):
    products = list(products)

    if not products:
        return None

    total_weight = sum(
        (product.weight for product in products),
        Decimal("0")
    )

    suitable_boxes = []

    for box in Box.objects.all():

        # Check total weight
        if total_weight > box.max_weight:
            continue

        # Check dimensions
        if all(can_product_fit_box(product, box) for product in products):
            suitable_boxes.append(box)

    if not suitable_boxes:
        return None

    # Select the lowest-cost suitable box
    return min(suitable_boxes, key=lambda box: box.cost)

2) this rejected becaused its used APIView 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import BoxRecommendationSerializer
from .services import recommend_box


class BoxRecommendationAPIView(APIView):

    def post(self, request):
        serializer = BoxRecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_ids = serializer.validated_data["product_ids"]

        products = Product.objects.filter(
            id__in=product_ids
        )

        # Check if all requested products exist
        if products.count() != len(set(product_ids)):
            return Response(
                {
                    "error": "One or more products were not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        box = recommend_box(products)

        if not box:
            return Response(
                {
                    "message": "No suitable box found."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "box": {
                    "id": box.id,
                    "name": box.name,
                    "internal_length": box.internal_length,
                    "internal_width": box.internal_width,
                    "internal_height": box.internal_height,
                    "max_weight": box.max_weight,
                    "cost": box.cost,
                }
            },
            status=status.HTTP_200_OK
        )

-- Any mistakes the AI made --
API endpoint for the box recommendation logic used APIView


-- verified final code -- 

    - running the django development server
    - testing API endpoints using Postman
    - testing products fit inside boxes or not
    - use test cases : test_api.py ,test_service.py