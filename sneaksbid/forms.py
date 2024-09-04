from datetime import timedelta
from decimal import Decimal
from django.contrib.auth.forms import UserChangeForm
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Payment2, Bid, Shoe, Brand


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Username',
        'id': 'username',
        'required': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Your Password',
        'id': 'password',
        'required': True}))


class PaymentForm(forms.Form):
    amount = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
        widget=forms.HiddenInput()
    )


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        widgets = {
            'bid_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        super(BidForm, self).__init__(*args, **kwargs)
        if self.item:
            self.fields['bid_amount'].widget.attrs['min'] = str(self.item.base_price + Decimal('0.01'))


class ShoeForm(forms.ModelForm):
    auction_duration_days = forms.IntegerField(min_value=0, initial=0, help_text='Days', required=False)
    auction_duration_hours = forms.IntegerField(min_value=0, max_value=23, initial=0, help_text='Hours', required=False)
    auction_duration_minutes = forms.IntegerField(min_value=0, max_value=59, initial=0, help_text='Minutes',
                                                  required=False)

    class Meta:
        model = Shoe
        fields = ['title', 'description', 'base_price', 'brand_name', 'image', 'size']

    def save(self, commit=True):
        days = self.cleaned_data.get('auction_duration_days', 0)
        hours = self.cleaned_data.get('auction_duration_hours', 0)
        minutes = self.cleaned_data.get('auction_duration_minutes', 0)

        total_duration = timedelta(days=days, hours=hours, minutes=minutes)

        self.instance.auction_duration = total_duration

        return super(ShoeForm, self).save(commit=commit)


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['images']


PAYMENT_CHOICES = [
    ('S', 'Stripe'),

]


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Country',
        'class': 'form-control'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Zip code',
        'class': 'form-control'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)


class ShoePriceRangeForm(forms.Form):
    minimum_price = forms.IntegerField(label='Minimum price', min_value=0, required=False)
    maximum_price = forms.IntegerField(label='Maximum price', min_value=0, required=False)

    def clean(self):
        cleaned_data = super().clean()
        minimum_price = cleaned_data.get('minimum_price')
        maximum_price = cleaned_data.get('maximum_price')

        if minimum_price and maximum_price and minimum_price > maximum_price:
            raise forms.ValidationError("Minimum price cannot be greater than maximum price")
        return cleaned_data

class BrandFilterForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label='Select Brand', required=False)


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {'name': forms.TextInput (attrs={'placeholder':'Enter A New Brand', 'class':'form-control'})}

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Check if a brand with the same name already exists
        if Brand.objects.filter(name=name).exists():
            raise forms.ValidationError("Brand with this name already exists.")

        return name