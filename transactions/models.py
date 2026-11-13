import uuid
 
from django.conf import settings
from django.db import models
 
 
class Transaction(models.Model):
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]
 
    def __str__(self):
        return f"Transaction {self.id} by {self.buyer}"
 
 
class ProductTransaction(models.Model):
    """ERD: product_transactions (line item of a transaction)."""
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.PositiveIntegerField()
    item = models.ForeignKey(
        "carts_products.Product",
        on_delete=models.PROTECT,
        related_name="product_transactions",
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="product_transactions",
    )
 
    class Meta:
        db_table = "product_transactions"
 
    def __str__(self):
        return f"{self.quantity} x {self.item.name}"