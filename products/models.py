from django.db import models
from django.core.validators import MaxLengthValidator
from django.db.models import Avg

from main.models import CloudinaryField, CustomUser

# category
class Category(models.Model):
    name = models.CharField(max_length=50, validators=[MaxLengthValidator], unique=True)
    manager = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


# product model.
# TODO: use uuid4 field to create a random primary key everytime. For security reasons.
class Product(models.Model):

    #class Meta:
    #    unique_together = (('user', 'product'),)

    name = models.CharField(null=False, blank=False, max_length=255, validators=[MaxLengthValidator,])
    quantity = models.IntegerField(default = 0)

    # max value = 99 999 999.99, 2 digits for decimal and 8 for other number.
    price = models.DecimalField(max_digits = 10, decimal_places=2, default = 0.00)
    is_special = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    description = models.TextField()
    full_description = models.TextField(null = True, blank=True)
    specifications = models.TextField(null = True, blank=True)
    categories = models.ManyToManyField(to=Category, related_name='productCategories', blank=True)
    managerOrMerchant = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True)
    front_image = CloudinaryField('images')
    rear_image = CloudinaryField('images')

    def __str__(self) -> str:
        return self.name + "  price: " + str(self.price) + " Quantity: " + str(self.quantity)
        
    def in_stock(self)-> bool:
        
        return True if self.quantity > 0 else False

    def get_average_stars(self) -> int:
        
        avg = (ProductReview.objects.filter(product = self.pk).aggregate(Avg('stars_count')))["stars_count__avg"]
        return avg if avg else 0.0


# product review
class ProductReview(models.Model):
    product = models.ForeignKey(to = Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True)

    stars_count = models.IntegerField(default=0)
    review = models.CharField(max_length=500, help_text='Maximum characters: 500', validators=[MaxLengthValidator])

    # only when created for the first time by calling .save().
    created = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)

    # change when this models is updated by calling .save().
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'product'),)

    def __str__(self) -> str:
        return self.user.username + " gave " + self.product.name + " " + str(self.stars_count) + " stars"
