from django.http import HttpResponse
from core.PayTM import Checksum
from django.contrib.auth.models import User
from django.db.models import Q  # new
import json
# import stripe
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.conf import settings
import random
import string
from django.http import JsonResponse

import requests
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'home.html'
    ordering = ['upload_date']


class SearchResultsView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'search.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')

        object_list = Item.objects.filter(
            Q(title__icontains=query) | Q(
                category__item_category__icontains=query) | Q(label__icontains=query)

        )
        return object_list


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.info(
                self.request, "No active orders found")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        context['suggestion'] = Item.objects.all()
        item = get_object_or_404(Item, slug=self.kwargs['slug'])
        context['itemimages'] = ItemImage.objects.filter(item=item)
        context['clothsize_choices'] = ClothSize.objects.filter(item=item)
        footwear_choices = FootwearSize.objects.filter(item=item)
        context['itemcolor_choices'] = ItemColor.objects.filter(item=item)
        context['stockquantity'] = StockQuantity.objects.filter(item=item)
        context['footwearsize_choices'] = footwear_choices
        # messages.info(
        #     self.request, "Only add items of same color and size to cart at a time. If size and color differs, order seperately else chosen attributes will be overwritten!!")
        return context


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # items = Item(slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():

            order_item.quantity += 1
            error = False
            error_text = ''
            if request.method == "POST":

                # if(item.is_footwear):
                #     order_item.footwear_size = request.POST['footwear_size']
                #     if(not order_item.footwear_size):
                #         error = True
                #         error_text = 'Please select an option'
                #         messages.warning(request, error_text)
                #         return redirect('product.html', slug=slug)

                #     order_item.save()
                #     item.save()

                # else:
                #     order_item.cloth_size = request.POST['cloth_size']

                #     order_item.save()
                #     item.save()

                # order_item.color = request.POST['footwear_cloth_color']
                order_item.save()
                item.save()
            messages.info(
                request, "Cart updated successfully")
            order_item.save()
            # items.stock_quantity -= 1
            item.save()

            return redirect("order-summary")

        else:
            if request.method == "POST":

                # if(item.is_footwear):
                #     order_item.footwear_size = request.POST['footwear_size']
                #     if(not order_item.footwear_size):
                #         error = True
                #         error_text = 'Please select an option'
                #         messages.warning(request, error_text)
                #         return redirect('product.html', slug=slug)
                #     order_item.save()
                #     item.save()

                # else:
                #     order_item.cloth_size = request.POST['cloth_size']
                #     order_item.save()
                #     item.save()
                # order_item.color = request.POST['footwear_cloth_color']
                order_item.save()

            order.items.add(order_item)
            messages.info(
                request, "Item added to cart successfully!!")

            return redirect("order-summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        error = False
        error_text = ''
        if request.method == "POST":

            # if(item.is_footwear):
            #     order_item.footwear_size = request.POST['footwear_size']
            #     if(not order_item.footwear_size):
            #         error = True
            #         error_text = 'Please select an option'
            #         messages.warning(request, error_text)
            #         return redirect('product.html', slug=slug)
            #     order_item.save()
            #     item.save()

            # else:
            #     order_item.cloth_size = request.POST['cloth_size']

            #     order_item.save()
            #     item.save()
            order_item.color = request.POST['footwear_cloth_color']
            order_item.save()
        messages.info(request, "Item added to cart successfully!!")
        order.items.add(order_item)
        return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.success(
                request, "This item was removed from your cart successfully!!")
            return redirect("order-summary")
        else:
            messages.warning(request, "Item not found in cart")
            return redirect("product", slug=slug)
    else:
        messages.warning(request, "Your cart is empty!!")
        return redirect("order-summary", slug=slug)


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(
                    request, "Cart updated successfully")
                return redirect("order-summary")
            else:
                order.items.remove(order_item)
                return redirect("order-summary")
        else:
            messages.info(request, "Item doesn't exist in your cart!")
            return redirect("product", slug=slug)
    else:
        messages.info(request, "No active orders found")
        return redirect("product", slug=slug)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                # elif payment_option == 'S':
                    # return redirect('payment', payment_option='stripe')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")


# stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_complete(request):
    body = json.loads(request.body)

    order = Order.objects.get(
        user=request.user, ordered=False, ref_code=body['orderid'])
    payment = Payment(
        user=request.user,
        paypal_transaction_id=body['payid'],
        amount=order.get_total()
    )
    payment.save()
    order.ordered = True
    order.payment = payment
    order.received = True
    order.save()
    # order_items = order.items.all()
    # order_items.update(ordered=True)

    # for item in order_items:
    #     st = StockQuantity.objects.filter(item=item.item)
    #     for each in st:
    #         print(each.stock_quantity)
    #     if st.stock_quantity > 0:
    #         st.stock_quantity -= item.quantity
    #         st.save()
    #         item.save()
    #     else:
    #         messages.warning("Item out of stock!!")
    #     print("Quantity " + str(st.stock_quantity))
    # order_item = OrderItem.objects.get(user=request.user, ordered=True)

    messages.success(request, "Order placed successfully!!")
    return redirect("/")


class PaymentView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            order.ref_code = create_ref_code()
            order.save()

            if order.billing_address:
                context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'amount': order.get_total()
                }

                return render(self.request, "payment.html", context)
            else:
                messages.warning(
                    self.request, "You have not added a billing address")
                return redirect("checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "No active orders found!")
            return redirect("/")

    '''def post(self, *args, **kwargs):
        return redirect("/")'''


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request, "This coupon does not exist")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(
                    self.request, "Coupon applied to cart successfully!!")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.warning(
                    self.request, "You do not have an active order")
                return redirect("checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.requested_refund = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("order_history")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("order_history")


@login_required
def show_user_profile(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'user': request.user,
        'profile': profile
    }
    return render(request, "user_profile.html", context)


class EditProfileView(View):

    def get(self, *args, **kwargs):
        user = self.request.user
        form = EditProfileForm()
        context = {
            'form': form,
        }
        return render(self.request, "edit_user_profile.html", context)

    def post(self, *args, **kwargs):
        form = EditProfileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            current_user = self.request.user
            profile = User.objects.get(id=current_user.id)
            if(profile.username != form.cleaned_data.get('username') and form.cleaned_data.get('username')):
                profile.username = form.cleaned_data.get('username')
                profile.save()
            profile = UserProfile.objects.get(user_id=current_user.id)
            if(profile.phone != form.cleaned_data.get('phone') and form.cleaned_data.get('phone')):
                profile.phone = form.cleaned_data.get('phone')
            if(profile.resident_address_1 != form.cleaned_data.get('resident_address_1') and form.cleaned_data.get('resident_address_1')):
                profile.resident_address_1 = form.cleaned_data.get(
                    'resident_address_1')
            if(profile.resident_address_2 != form.cleaned_data.get('resident_address_2') and form.cleaned_data.get('resident_address_2')):
                profile.resident_address_2 = form.cleaned_data.get(
                    'resident_address_2')
            if(profile.pincode != form.cleaned_data.get('pincode') and form.cleaned_data.get('pincode')):
                profile.pincode = form.cleaned_data.get('pincode')
            if(profile.state != form.cleaned_data.get('state') and form.cleaned_data.get('state')):
                profile.state = form.cleaned_data.get('state')
            if(profile.city != form.cleaned_data.get('city') and form.cleaned_data.get('city')):
                profile.city = form.cleaned_data.get('city')
            if(form.cleaned_data.get('image')):
                profile.image = form.cleaned_data.get('image')
            profile.save()
        messages.success(self.request, "Profile updated successfully!!")
        return redirect('user_profile')


@login_required
def OrderHistory(request):
    try:
        order_qs = Order.objects.filter(
            user=request.user, ordered=True).order_by('-ordered_date')
        # length_qs = len(order_qs)
        items = OrderItem.objects.filter(user=request.user, ordered=True)
        profile = UserProfile.objects.get(user=request.user)
        context = {
            'user': request.user,
            'order_qs': order_qs,
            'items': items,
            'profile': profile
        }
        print(order_qs[0].items)
        return render(request, "order_history.html", context)
    except Exception as e:
        messages.warning(request, "No previous Orders found!")
        return redirect('home')


'''
def Category(request):
    items_all = Item.objects.all()
    items_shoes_qs = Item.objects.filter(category='Shoes')
    items_tshirts_qs = Item.objects.filter(category='T-Shirts')
    items_outwear_qs = Item.objects.filter(category='Outwear')
    items_jeans_qs = Item.objects.filter(category='Jeans')
    items_sportswear_qs = Item.objects.filter(category='Sports wear')
    context = {
        'items_all': items_all,
        'items_shoes_qs': items_shoes_qs,
        'items_tshirts_qs': items_tshirts_qs,
        'items_outwear_qs': items_outwear_qs,
        'items_jeans_qs': items_jeans_qs,
        'items_sportswear_qs': items_sportswear_qs
    }
    return render(request, 'category.html', context)
'''
