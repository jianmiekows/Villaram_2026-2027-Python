from django.contrib import admin

from .models import Cart, CartProduct, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "stock", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "sku")


class CartProductInline(admin.TabularInline):
    model = CartProduct
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "created_at", "updated_at")
    inlines = [CartProductInline]


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")