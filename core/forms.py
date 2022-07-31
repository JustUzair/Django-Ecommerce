from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# tuples
PAYMENT_CHOICES = (
    # ('S', 'Stripe'),
    ('P', 'PayPal'),
    # ('PTM', 'Paytm'),
    # ('COD', 'CashOnDelivery'),
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code',
        'aria-label': "Recipient's username",
        'aria-describedby': 'basic-addon2',
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)


class EditProfileForm(forms.Form):

    username = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    resident_address_1 = forms.CharField(required=False)
    resident_address_2 = forms.CharField(required=False)
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    pincode = forms.CharField(required=False)
    image = forms.ImageField(required=False)


CLOTH_SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
)

FOOTWEAR_SIZE_CHOICES = (
    ('6', '6'),
    ('6.5', '6.5'),
    ('7', '7'),
    ('7.5', '7.5'),
    ('8', '8'),
    ('8.5', '8.5'),
    ('9', '9'),
    ('10', '10'),
)

COLOR_CHOICES = (
    ('White', 'White'),
    ('Black', 'Black'),
    ('Green', 'Green'),
    ('Blue', 'Blue'),
)


class ProductAttribute(forms.Form):
    footwear_size = forms.ChoiceField(
        widget=forms.RadioSelect, choices=CLOTH_SIZE_CHOICES)
    cloth_size = forms.ChoiceField(
        widget=forms.RadioSelect, choices=FOOTWEAR_SIZE_CHOICES)
    color = forms.ChoiceField(widget=forms.RadioSelect, choices=COLOR_CHOICES)
