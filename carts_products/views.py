from django.db import transaction
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartProduct, Product
from .serializers import (
    AddCartItemSerializer,
    CartSerializer,
    ProductSerializer,
    UpdateCartItemSerializer,
)
from .services import cart_with_items, get_user_cart


# --------------------------------------------------------------------------- #
# Products
# --------------------------------------------------------------------------- #
class ProductPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_staff


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = Product.objects.all()
        user = self.request.user
        if not (user.is_authenticated and user.is_staff):
            queryset = queryset.filter(is_active=True)
        search = self.request.query_params.get("search")
        if search and self.action == "list":
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            instance.is_active = False
            instance.save(update_fields=["is_active", "updated_at"])

def _cart_response(cart, request, status_code=status.HTTP_200_OK):
    data = CartSerializer(cart_with_items(cart), context={"request": request}).data
    return Response(data, status=status_code)


def _touch(cart):
    cart.save(update_fields=["updated_at"])


class CartView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return _cart_response(get_user_cart(request.user), request)

    def delete(self, request):
        cart = get_user_cart(request.user)
        cart.cart_products.all().delete()
        _touch(cart)
        return _cart_response(cart, request)


class CartItemCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart = get_user_cart(request.user)
        with transaction.atomic():
            item = CartProduct.objects.filter(cart=cart, product=product).first()
            new_quantity = (item.quantity if item else 0) + quantity
            if new_quantity > product.stock:
                raise ValidationError({"quantity": f"Only {product.stock} in stock."})
            if item:
                item.quantity = new_quantity
                item.save(update_fields=["quantity"])
            else:
                CartProduct.objects.create(cart=cart, product=product, quantity=new_quantity)
            _touch(cart)
        return _cart_response(cart, request, status.HTTP_201_CREATED)


class CartItemDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def _get_item(self, request, pk):
        return get_object_or_404(
            CartProduct.objects.select_related("cart", "product"),
            pk=pk,
            cart__owner=request.user,
        )

    def patch(self, request, pk):
        item = self._get_item(request, pk)
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        if quantity > item.product.stock:
            raise ValidationError({"quantity": f"Only {item.product.stock} in stock."})
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        _touch(item.cart)
        return _cart_response(item.cart, request)

    def delete(self, request, pk):
        item = self._get_item(request, pk)
        cart = item.cart
        item.delete()
        _touch(cart)
        return _cart_response(cart, request)