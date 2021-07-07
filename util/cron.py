from product.models import Discount


def discount_manager():
    for model in Discount.objects.all():
        model.product_set.update(discount_available=model.is_discount)
