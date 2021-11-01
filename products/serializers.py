from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from . import models

# category serializer
class CategorySerializer(serializers.ModelSerializer):
     class Meta:
         model = models.Category
         fields =['Name']


class ProductManagerSerializer(serializers.ModelSerializer):

    FrontImage = serializers.SerializerMethodField(read_only=False)
    RearImage = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = models.Product
        fields = ['id', 'Name', 'Quantity', 'Price', 'isSpecial', 'isActive', 'Description', 'FrontImage', 'RearImage']

    def get_RearImage(self, obj):
        return obj.RearImage.url if obj.RearImage else None

    def get_FrontImage(self, obj):

        return obj.FrontImage.url if obj.FrontImage else None


# get product for display only
class ProductDisplaySerializer(serializers.ModelSerializer):

    FrontImage = serializers.SerializerMethodField(read_only=True)
    RearImage = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Product
        fields = ['Name', 'Quantity', 'Price', 'Description', 'FrontImage', 'RearImage', 'id']

    def get_id(self, obj):
        return obj.pk

    def get_RearImage(self, obj):
        return obj.RearImage.url if obj.RearImage else None

    def get_FrontImage(self, obj):

        return obj.FrontImage.url if obj.FrontImage else None


# product review serializer
class ProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductReview
        fields = ['id', 'starsCount', 'review', 'user', 'product']