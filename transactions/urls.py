from django.urls import path

from .views import CheckoutView, TransactionDetailView, TransactionListView

urlpatterns = [
    path("transactions/", TransactionListView.as_view(), name="transaction-list"),
    path("transactions/checkout/", CheckoutView.as_view(), name="checkout"),
    path("transactions/<uuid:pk>/", TransactionDetailView.as_view(), name="transaction-detail"),
]