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