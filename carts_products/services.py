from .models import Cart


def get_user_cart(user):
    """Return the user's current cart (their newest one), creating it if needed."""
    cart = user.carts.order_by("-created_at").first()
    if cart is None:
        cart = Cart.objects.create(owner=user)
    return cart


def cart_with_items(cart):
    """Reload a cart with its items and products prefetched (avoids N+1 queries)."""
    return Cart.objects.prefetch_related("cart_products__product").get(pk=cart.pk)