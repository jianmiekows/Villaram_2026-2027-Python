from django.db import transaction
from django.db.models import F
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from carts_products.models import Product
from carts_products.services import get_user_cart

from .models import ProductTransaction, Transaction
from .serializers import TransactionSerializer


def _user_transactions(user):
    return (
        Transaction.objects.filter(buyer=user)
        .prefetch_related("product_transactions__item")
        .order_by("-created_at")
    )


class TransactionListView(generics.ListAPIView):
    """GET /api/transactions/ - the logged-in user's purchase history."""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _user_transactions(self.request.user)


class TransactionDetailView(generics.RetrieveAPIView):
    """GET /api/transactions/<id>/ - one of the user's own purchases."""

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _user_transactions(self.request.user)


class CheckoutView(APIView):
    """POST /api/transactions/checkout/

    Turns the cart into a Transaction: every cart line becomes a ProductTransaction,
    stock is reduced, and the cart is emptied. All or nothing.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_user_cart(request.user)
        lines = list(cart.cart_products.all())
        if not lines:
            raise ValidationError({"detail": "Your cart is empty."})

        with transaction.atomic():
            # lock the product rows so two checkouts can't oversell the same stock
            products = Product.objects.select_for_update().in_bulk(
                [line.product_id for line in lines]
            )

            problems = []
            for line in lines:
                product = products[line.product_id]
                if not product.is_active:
                    problems.append(f"{product.name} is no longer available.")
                elif line.quantity > product.stock:
                    problems.append(f"Only {product.stock} of {product.name} left in stock.")
            if problems:
                raise ValidationError({"detail": problems})

            purchase = Transaction.objects.create(buyer=request.user)
            ProductTransaction.objects.bulk_create(
                [
                    ProductTransaction(
                        transaction=purchase, item_id=line.product_id, quantity=line.quantity
                    )
                    for line in lines
                ]
            )
            for line in lines:
                Product.objects.filter(pk=line.product_id).update(
                    stock=F("stock") - line.quantity
                )
            cart.cart_products.all().delete()

        purchase = _user_transactions(request.user).get(pk=purchase.pk)
        data = TransactionSerializer(purchase, context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)