from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from .models import Product, Box
from .serializers import ProductSerializer, BoxSerializer, BoxRecommendationSerializer
from rest_framework.decorators import action
from .services import recommend_box


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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