from datetime import datetime, timedelta
import uuid
from django.core.validators import MaxLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField as BaseCloudinaryField

from main.utils import get_future_date

class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
            'public_id': model_instance.name,
            'unique_filename': False,
            'overwrite': True,
            'resource_type': 'image',
            'tags': ['profile', 'profile-map'],
            'invalidate': True,
            'quality': 'auto:eco',

        }


# abstract user
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username


# user profile
class UserProfile(models.Model):
    Biography = models.TextField()
    Country = models.CharField(max_length = 150, validators=[MaxLengthValidator], null=True, blank=True)
    Contact = models.CharField(max_length = 50, validators=[MaxLengthValidator], null=True, blank=True)
    HeaderImage = CloudinaryField('images')
    Avatar = CloudinaryField('images')
    isSeller = models.BooleanField(default = False)
    isManager = models.BooleanField(default = False)
    loyaltyPoints = models.IntegerField(default = 0)
    user = models.OneToOneField(to = CustomUser,  on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username


# coupon model
class Coupon(models.Model):

    # max value: 9.99, 2 digits for decimal point and 1 for other.
    amount = models.DecimalField(max_digits = 3, decimal_places = 2)
    Code = models.UUIDField(default=uuid.uuid4, unique=True)
    isValid = models.BooleanField(default = True)
    createdDate = models.DateTimeField(auto_now_add = True)
    expiredDate = models.DateTimeField()
    admin = models.ForeignKey(to = CustomUser, on_delete = models.SET_NULL, null = True)

    def __str__(self):

        if(self.expiredDate.timestamp() <= datetime.now().timestamp()):
            self.isValid = False
            self.save()

        return self.admin.username + "  --- amount: " + str(self.amount)







