from django.db import models
from django.contrib.auth.models import User 
from datetime import timedelta

# Create your models here.
class Resort(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='resorts/', default='resorts/default.jpg')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resorts')

class Meta:
        permissions = [
            ("can_edit_own_resort", "Can edit own resort"),
            ("can_edit_any_resort", "Can edit any resort"),
        ]

def __str__(self):
        return self.name

  


class Booking(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # New field for approval

    def __str__(self):
        return f"Booking for {self.resort.name} by {self.user.username}"

    def calculate_total_price(self):
        # Get the number of nights
        number_of_nights = (self.check_out_date - self.check_in_date).days
        # Ensure the number of nights is at least 1
        if number_of_nights < 1:
            number_of_nights = 1
        # Calculate the total price based on resort's price per night
        return self.resort.price_per_night * number_of_nights




