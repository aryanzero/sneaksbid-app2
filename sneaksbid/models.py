from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from djstripe.models import StripeModel
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your models here.
class Brand(models.Model):
    # brand_lists = [
    #     ('Nike', 'N'),
    #     ('Adidas', 'A'),
    #     ('Puma', 'P'),
    #     ('Reebok', 'R'),
    # ]
    # name = models.TextField(max_length=100, choices=brand_lists, default='Nike')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    post_time = models.DateTimeField(default=timezone.now)
    auction_duration = models.DurationField(default=timezone.timedelta(days=1))  # Auction lasts for 1 day
    image = models.ImageField(upload_to='items/')
    available = models.BooleanField(default=True)

    @property
    def is_auction_active(self):
        now = timezone.now()
        auction_end_time = self.post_time + self.auction_duration
        return self.post_time <= now <= auction_end_time

    @property
    def duration_days(self):
        return self.auction_duration.days

    @property
    def duration_hours(self):
        return self.auction_duration.seconds // 3600

    @property
    def duration_minutes(self):
        return (self.auction_duration.seconds % 3600) // 60

    def __str__(self):
        return self.title



# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Item, through='CartItem')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Cart for {self.user.username}"
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} of {self.item.title} in Cart for {self.cart.user.username}" 


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)  # Add this field to indicate the winning bid

    def __str__(self):
        return f"{self.user.username} - {self.bid_amount} - {self.is_winner}"




class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.current_bid


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=100)
    same_shipping_address = models.BooleanField(default=False)
    save_info = models.BooleanField(default=False)
    payment_option = models.CharField(max_length=10)  # Assuming you store the choice as a string

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_delivered = models.BooleanField(default=False)
    order_received = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_ordered_price(self):
        total_price = 0
        for ordered_item in self.ordered_items.all():
            total_price += ordered_item.price
        return total_price


class Payment2(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user.username


class Shoe(Item):
    # Add shoe-specific fields here if needed, for example:
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.title} - {self.size}"


from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
