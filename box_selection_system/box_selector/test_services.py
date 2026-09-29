from decimal import Decimal
from django.test import TestCase
from box_selector.models import Product, Box
from box_selector.services import recommend_box

class BoxRecommendationServiceTest(TestCase):

    def setUp(self):
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
  
    def test_single_product_returns_suitable_box(self):
        product = self.create_product(
            length=10,
            width=10,
            height=5,
            weight=1,
        )

        result = recommend_box([product])

        self.assertEqual(result, self.small_box)

    def test_multiple_products_returns_suitable_box(self):
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

        result = recommend_box([product1, product2])

        self.assertEqual(result, self.small_box)

    def test_exact_dimension_match_is_allowed(self):
        product = self.create_product(
            length=20,
            width=15,
            height=10,
            weight=5,
        )

        result = recommend_box([product])

        self.assertEqual(result, self.small_box)

    def test_exact_weight_match_is_allowed(self):
        product = self.create_product(
            length=10,
            width=10,
            height=5,
            weight=5,
        )

        result = recommend_box([product])

        self.assertEqual(result, self.small_box)

    def test_total_weight_of_multiple_products_is_checked(self):
        product1 = self.create_product(
            name="Product 1",
            weight=2,
        )

        product2 = self.create_product(
            name="Product 2",
            weight=2,
        )

        result = recommend_box([product1, product2])

        self.assertEqual(result, self.small_box)

    # LOWEST COST
    
    def test_lowest_cost_suitable_box_is_returned(self):
        product = self.create_product(
            length=10,
            width=10,
            height=5,
            weight=1,
        )

        result = recommend_box([product])

        self.assertEqual(result.cost, Decimal("20.00"))
        self.assertEqual(result, self.small_box)

    # DIMENSION FAILURE

    def test_product_length_greater_than_box_fails(self):
        product = self.create_product(
            length=21,
            width=10,
            height=5,
            weight=1,
        )

        result = recommend_box([product])

        self.assertEqual(result, self.medium_box)

    def test_product_that_exceeds_all_box_dimensions_returns_none(self):
        product = self.create_product(
            length=60,
            width=50,
            height=40,
            weight=1,
        )

        result = recommend_box([product])

        self.assertIsNone(result)

    # WEIGHT FAILURE
    

    def test_product_weight_greater_than_small_box_uses_larger_box(self):
        product = self.create_product(
            length=10,
            width=10,
            height=5,
            weight=6,
        )

        result = recommend_box([product])

        self.assertEqual(result, self.medium_box)

    def test_total_weight_greater_than_small_box_uses_larger_box(self):
        product1 = self.create_product(
            name="Product 1",
            weight=3,
        )

        product2 = self.create_product(
            name="Product 2",
            weight=3,
        )

        result = recommend_box([product1, product2])

        self.assertEqual(result, self.medium_box)

    def test_weight_greater_than_all_boxes_returns_none(self):
        product = self.create_product(
            weight=25,
        )

        result = recommend_box([product])

        self.assertIsNone(result)

    # MULTIPLE PRODUCT FILAI

    def test_if_one_product_does_not_fit_box_larger_box_is_selected(self):
        product1 = self.create_product(
            name="Product 1",
            length=10,
            width=10,
            height=5,
        )

        product2 = self.create_product(
            name="Product 2",
            length=25,
            width=10,
            height=5,
        )

        result = recommend_box([product1, product2])

        self.assertEqual(result, self.medium_box)

    def test_multiple_products_with_one_too_large_for_all_boxes_returns_none(self):
        product1 = self.create_product(
            name="Valid Product",
            length=10,
            width=10,
            height=5,
        )

        product2 = self.create_product(
            name="Oversized Product",
            length=60,
            width=50,
            height=40,
        )

        result = recommend_box([product1, product2])

        self.assertIsNone(result)

    # EDGE CASES

    def test_empty_product_list_returns_none(self):
        result = recommend_box([])

        self.assertIsNone(result)

    def test_no_boxes_available_returns_none(self):
        Box.objects.all().delete()

        product = self.create_product()

        result = recommend_box([product])

        self.assertIsNone(result)

    def test_zero_products_returns_none(self):
        result = recommend_box([])

        self.assertIsNone(result)