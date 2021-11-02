from django.db import models
from django.core.validators import MaxLengthValidator

from main.models import CloudinaryField, CustomUser

# category
class Category(models.Model):
    Name = models.CharField(max_length=50, validators=[MaxLengthValidator], unique=True)
    manager = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.Name


# product model.
# TODO: use uuid4 field to create a random primary key everytime. For security reasons.
class Product(models.Model):

    #class Meta:
    #    unique_together = (('user', 'product'),)

    Name = models.CharField(null=False, blank=False, max_length=255, validators=[MaxLengthValidator,])
    Quantity = models.IntegerField(default = 0)

    # max value = 99 999 999.99, 2 digits for decimal and 8 for other number.
    Price = models.DecimalField(max_digits = 10, decimal_places=2, default = 0.00)
    isSpecial = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)
    Description = models.TextField()
    Categories = models.ManyToManyField(to=Category, related_name='productCategories', blank=True)
    managerOrMerchant = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True)
    FrontImage = CloudinaryField('images')
    RearImage = CloudinaryField('images')

    def __str__(self) -> str:
        return self.Name + "  price: " + str(self.Price) + " Quantity: " + str(self.Quantity)


# product review
class ProductReview(models.Model):
    product = models.ForeignKey(to = Product, on_delete=models.CASCADE)
    user = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True)

    starsCount = models.IntegerField(default=0)
    review = models.CharField(max_length=500, help_text='Maximum characters: 500', validators=[MaxLengthValidator])

    # only when created for the first time by calling .save().
    created = models.DateTimeField(auto_now_add=True)
    isEdited = models.BooleanField(default=False)

    # change when this models is updated by calling .save().
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'product'),)

    def __str__(self) -> str:
        return self.user.username + " gave " + self.product.Name + " " + str(self.product.starsCount) + " stars"
