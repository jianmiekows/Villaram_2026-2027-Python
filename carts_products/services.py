from .models import Cart


def get_user_cart(user):
    cart = Cart.objects.filter(owner=user).order_by("created_at").first()
    return cart or Cart.objects.create(owner=user)


def cart_with_items(cart):
    return Cart.objects.prefetch_related("cart_products__product").get(pk=cart.pk)