from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CartItemCreateView, CartItemDetailView, CartView, ProductViewSet

router = SimpleRouter()
router.register("products", ProductViewSet, basename="product")

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/items/", CartItemCreateView.as_view(), name="cart-item-add"),
    path("cart/items/<uuid:pk>/", CartItemDetailView.as_view(), name="cart-item-detail"),
] + router.urls