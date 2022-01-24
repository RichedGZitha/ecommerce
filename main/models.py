from datetime import datetime, timedelta
import uuid
from django.core.validators import MaxLengthValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
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
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self) -> str:
        return self.username


# user profile
class UserProfile(models.Model):
    biography = models.TextField()
    country = models.CharField(max_length = 256, validators=[MaxLengthValidator], null=True, blank=True)
    
    street_address =  models.CharField(null=True, blank=True, max_length= 500 , validators=[MaxLengthValidator])
    suburb =  models.CharField(null=True, blank=True, max_length= 500 , validators=[MaxLengthValidator])
    city =  models.CharField(null=True, blank=True, max_length= 500 , validators=[MaxLengthValidator])
    province = models.CharField(null=True, blank=True, max_length= 500 , validators=[MaxLengthValidator])
    postal_code = models.CharField(null=True, blank=True, max_length= 500 , validators=[MaxLengthValidator])
    
    contact_number = models.CharField(max_length = 50, validators=[MaxLengthValidator], null=True, blank=True)
    header_image = CloudinaryField('images')
    avatar = CloudinaryField('images')
    is_seller = models.BooleanField(default = False)
    is_manager = models.BooleanField(default = False)
    loyalty_points = models.IntegerField(default = 0)
    user = models.OneToOneField(to = CustomUser,  on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username


# coupon model
class Coupon(models.Model):

    # max value: 9.99, 2 digits for decimal point and 1 for other.
    amount = models.DecimalField(max_digits = 3, decimal_places = 2) 
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    is_valid = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    expired_date = models.DateTimeField()
    admin = models.ForeignKey(to = CustomUser, on_delete = models.SET_NULL, null = True)

    def __str__(self):

        if(self.expiredDate.timestamp() <= datetime.now().timestamp()):
            self.isValid = False
            self.save()

        return self.admin.username + "  --- amount: " + str(self.amount)







