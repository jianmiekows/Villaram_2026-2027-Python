from rest_framework import serializers

from .models import Cart, CartProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "sku",
            "price",
            "stock",
            "thumbnail",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {"price": {"min_value": 0}}


class CartProductSerializer(serializers.ModelSerializer):
    """One line in the cart (read-only view of product + quantity)."""

    product = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ["id", "product", "quantity", "subtotal"]

    def get_subtotal(self, obj):
        return f"{obj.product.price * obj.quantity:.2f}"


class CartSerializer(serializers.ModelSerializer):
    items = CartProductSerializer(source="cart_products", many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "owner", "items", "total", "created_at", "updated_at"]
        read_only_fields = fields

    def get_total(self, obj):
        total = sum(line.product.price * line.quantity for line in obj.cart_products.all())
        return f"{total:.2f}"


class AddCartItemSerializer(serializers.Serializer):
    """Body for POST /api/cart/items/ -> {"product_id": "<uuid>", "quantity": 2}"""

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True), source="product"
    )
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    """Body for PATCH /api/cart/items/<id>/ -> {"quantity": 3}"""

    quantity = serializers.IntegerField(min_value=1)