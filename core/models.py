from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.

CATEGORY_CHOICES = (
    ('Shirt', 'Shirt'),
    ('Sports wear', 'Sports wear'),
    ('Outwear', 'Outwear'),
    ('Shoes', 'Shoes'),
    ('Jeans', 'Jeans'),
    ('T-Shirts', 'T-Shirts'),
    ('Other', 'Other')
)
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
)


def item_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'items/%s.%s' % (instance.item.title, extension)


class ItemImage(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True,
                              upload_to=item_upload_location, default='no-product-image.jpg')

    def __str__(self):
        return self.item.title


def item_cover_upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'items/cover/%s.%s' % (instance.title, extension)


class Category(models.Model):
    item_category = models.CharField(
        max_length=25, null=True, blank=True)

    def __str__(self):
        return self.item_category

    class Meta:
        verbose_name_plural = "Categories"


class ItemColor(models.Model):
    item_color = models.CharField(
        max_length=25, null=True, blank=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return self.item_color


class ClothSize(models.Model):
    cloth_size = models.CharField(
        max_length=25, null=True, blank=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return self.cloth_size


class FootwearSize(models.Model):
    footwear_size = models.CharField(
        max_length=25, null=True, blank=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        if self.item.is_footwear:
            return self.footwear_size


class StockQuantity(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    color = models.ForeignKey(
        'ItemColor', on_delete=models.CASCADE)
    cloth_size = models.ForeignKey(
        'ClothSize', on_delete=models.CASCADE, blank=True, null=True)
    footwear_size = models.ForeignKey(
        'FootwearSize', on_delete=models.CASCADE, blank=True, null=True)
    stock_quantity = models.IntegerField(null=True, default=10)

    class Meta:
        verbose_name_plural = "Stock Quantities"

    def __str__(self):
        default_error_messages = {
            'invalid_choice': (u"Can't select both option"),
        }
        if self.footwear_size:
            return self.color.item.title + ': ' + str(self.footwear_size) + ', ' + str(self.color)
        elif self.cloth_size:
            return self.color.item.title + ': ' + str(self.cloth_size) + ', ' + str(self.color)
        else:
            self.error_messages['invalid']


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    stock_quantity = models.IntegerField(blank=True, null=True)
    '''stockquantity = models.ForeignKey(
        'StockQuantity', on_delete=models.CASCADE, null=True, blank=True)'''
    cover_image = models.ImageField(blank=True, null=True,
                                    upload_to=item_cover_upload_location, default='no-product-image.jpg')

    is_footwear = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    footwear_size = models.CharField(max_length=50, null=True)
    cloth_size = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=50, null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order of {self.quantity}  {self.item.title} by {self.user}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    requested_refund = models.BooleanField(default=False)
    refund_status = models.BooleanField(default=False)
    # size = models.CharField(blank=True, null=True)
    '''
        1.Item added to cart
        2.Adding  a Billing Address
        (Failed Checkout)
        3.Payment
        4.Delivery of Product
        5.Received
        6.Refunds
    '''

    def __str__(self):
        if self.ordered == 'True':
            return self.user.username + ' ' + self.ordered_date
        else:
            return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            if self.coupon.code == 'GRAND30':
                if total > 200:
                    total -= self.coupon.amount
                    if total <= 0:
                        total += 100
            elif self.coupon.code == 'DISCOUNT10':
                total -= self.coupon.amount
                if total <= 0:
                    total += 15
            else:
                pass

        return total


ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),


)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    paypal_transaction_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

# UserProfile


def upload_location(instance, filename):
    filebase, extension = filename.split('.')
    return 'users/%s/%s.%s' % (instance.user.id, instance.user.username, extension)


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=35, blank=True)
    state = models.CharField(max_length=35, blank=True)
    pincode = models.CharField(max_length=7, blank=True, null=True)
    resident_address_1 = models.CharField(max_length=100, blank=True)
    resident_address_2 = models.CharField(
        max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=upload_location, null=True,
                              blank=True, default='no-profile.png')

    def __str__(self):
        return self.user.username

    def Resident_address(self):
        if self.resident_address_1 is None:
            self.resident_address_1 = ''
        if self.resident_address_2 is None:
            self.resident_address_2 = ''
            return self.resident_address_1 + self.resident_address_2
        return self.resident_address_1 + ', ' + self.resident_address_2

    def image_tag(self):
        return mark_safe('<img src="{}" height="70" width="70" style="border-radius:100px"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def user_name(self):
        return self.user.username


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
