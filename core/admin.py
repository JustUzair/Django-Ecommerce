from django.contrib import admin
from .models import *

# Register your models here.


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(requested_refund=False, refund_status=True)


def out_for_delivery(modeladmin, request, queryset):
    queryset.update(being_delivered=True)


make_refund_accepted.short_description = 'Update orders to refund granted'
out_for_delivery.short_description = 'Update Order to "Out for Delivery"'


class OrderAdmin(admin.ModelAdmin):

    list_display = ['user', 'ordered_date', 'ordered', 'being_delivered',
                    'received', 'requested_refund', 'refund_status', 'coupon'] + ['payment']
    list_display_links = ['user', 'coupon'] + ['payment']
    list_filter = ['ordered', 'being_delivered',
                   'received', 'requested_refund', 'refund_status']
    search_fields = [
        'user__username',
        'ref_code',
    ]
    actions = [make_refund_accepted, out_for_delivery]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['user_name', 'Resident_address',
                    'phone', 'city', 'state', 'image_tag']


class StockQuantityAdmin(admin.ModelAdmin):
    list_display = ['item__is_footwear']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(ItemImage)
admin.site.register(Category)
admin.site.register(ItemColor)
admin.site.register(ClothSize)
admin.site.register(FootwearSize)
admin.site.register(StockQuantity)
admin.site.register(UserProfile, UserProfileAdmin)
