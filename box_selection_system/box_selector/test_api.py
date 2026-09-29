from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Product, Box

class BoxRecommendationAPITest(APITestCase):

    def setUp(self):
        self.url = reverse("boxes-recommend")

        self.small_box = Box.objects.create(
            name="Small Box",
            internal_length=20,
            internal_width=15,
            internal_height=10,
            max_weight=5,
            cost=20,
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            internal_length=30,
            internal_width=20,
            internal_height=15,
            max_weight=10,
            cost=40,
        )

        self.large_box = Box.objects.create(
            name="Large Box",
            internal_length=50,
            internal_width=40,
            internal_height=30,
            max_weight=20,
            cost=70,
        )

    def create_product(
        self,
        name="Product",
        length=10,
        width=10,
        height=5,
        weight=1,
    ):
        return Product.objects.create(
            name=name,
            length=length,
            width=width,
            height=height,
            weight=weight,
        )

    # VALID CASES

    def test_recommend_box_for_single_product(self):
        product = self.create_product()

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["box"]["id"],
            self.small_box.id
        )

    def test_recommend_box_for_multiple_products(self):
        product1 = self.create_product(
            name="Product 1",
            length=10,
            width=10,
            height=5,
            weight=1,
        )

        product2 = self.create_product(
            name="Product 2",
            length=15,
            width=10,
            height=5,
            weight=2,
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [
                    product1.id,
                    product2.id
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["box"]["id"],
            self.small_box.id
        )

    def test_returns_lowest_cost_suitable_box(self):
        product = self.create_product()

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["box"]["id"],
            self.small_box.id
        )
        self.assertEqual(
            response.data["box"]["cost"],
            "20.00"
        )

    def test_exact_dimensions_are_accepted(self):
        product = self.create_product(
            length=20,
            width=15,
            height=10,
            weight=5,
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["box"]["id"],
            self.small_box.id
        )

    def test_exact_max_weight_is_accepted(self):
        product = self.create_product(
            weight=5
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["box"]["id"],
            self.small_box.id
        )

    # =========================================================
    # DIMENSION CASES
    # =========================================================

    def test_length_exceeding_small_box_selects_larger_box(self):
        product = self.create_product(
            length=21,
            width=10,
            height=5,
            weight=1,
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["box"]["id"],
            self.medium_box.id
        )
    # =========================================================
    # WEIGHT CASES
    # =========================================================

    def test_multiple_product_total_weight_is_checked(self):
        product1 = self.create_product(
            name="Product 1",
            weight=3,
        )

        product2 = self.create_product(
            name="Product 2",
            weight=3,
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [
                    product1.id,
                    product2.id
                ]
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["box"]["id"],
            self.medium_box.id
        )

    # =========================================================
    # INVALID PRODUCT IDS
    # =========================================================

    def test_non_existing_product_id_returns_404(self):
        response = self.client.post(
            self.url,
            {
                "product_ids": [99999]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        self.assertEqual(
            response.data["error"],
            "One or more products were not found."
        )

    def test_mix_of_existing_and_non_existing_products_returns_404(self):
        product = self.create_product()

        response = self.client.post(
            self.url,
            {
                "product_ids": [
                    product.id,
                    99999
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    # =========================================================
    # NO SUITABLE BOX
    # =========================================================

    def test_no_box_can_fit_product_returns_400(self):
        product = self.create_product(
            length=100,
            width=100,
            height=100,
            weight=1,
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["message"],
            "No suitable box found."
        )

    def test_product_weight_exceeds_all_boxes_returns_400(self):
        product = self.create_product(
            weight=25
        )

        response = self.client.post(
            self.url,
            {
                "product_ids": [product.id]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.data["message"],
            "No suitable box found."
        )
