from rest_framework import serializers

from carts_products.serializers import ProductSerializer

from .models import ProductTransaction, Transaction


class ProductTransactionSerializer(serializers.ModelSerializer):
    item = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ProductTransaction
        fields = ["id", "item", "quantity", "subtotal"]

    def get_subtotal(self, obj):
        # NOTE: the ERD stores no price on a transaction line, so this uses the
        # product's current price.
        return f"{obj.item.price * obj.quantity:.2f}"


class TransactionSerializer(serializers.ModelSerializer):
    items = ProductTransactionSerializer(source="product_transactions", many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["id", "buyer", "items", "total", "created_at"]
        read_only_fields = fields

    def get_total(self, obj):
        total = sum(line.item.price * line.quantity for line in obj.product_transactions.all())
        return f"{total:.2f}"