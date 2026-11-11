from django.contrib import admin

from .models import ProductTransaction, Transaction


class ProductTransactionInline(admin.TabularInline):
    model = ProductTransaction
    extra = 0


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "created_at")
    inlines = [ProductTransactionInline]


@admin.register(ProductTransaction)
class ProductTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction", "item", "quantity")