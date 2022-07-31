from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>',
         remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path("request-refund/", RequestRefundView.as_view(), name="request-refund"),
    path('search/', SearchResultsView.as_view(), name='search'),
    path('payment-complete/', payment_complete, name='payment_complete'),
    path('user-profile/', show_user_profile, name="user_profile"),
    path('edit-user-profile/', EditProfileView.as_view(), name="edit_user_profile"),
    path('order-history/', OrderHistory, name="order_history"),
    # path('update-profile/', update_user_profile,name="update_user_profile"),
    # path('category/', Category, name='category'),
]
