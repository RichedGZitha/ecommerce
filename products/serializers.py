import random
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from . import models

# category serializer
class CategorySerializer(serializers.ModelSerializer):
     class Meta:
         model = models.Category
         fields =['name']


class ProductManagerSerializer(serializers.ModelSerializer):

    front_image = serializers.SerializerMethodField(read_only=False)
    rear_image = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'quantity', 'price', 'is_special', 'is_active', 'description', 'front_image', 'rear_image']

    def get_rear_image(self, obj):
        return obj.rear_image.url if obj.rear_image else None

    def get_front_image(self, obj):

        return obj.front_image.url if obj.front_image else None


# get product for display only
class ProductDisplaySerializer(serializers.ModelSerializer):

    front_image = serializers.SerializerMethodField(read_only=True)
    rear_image = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only = True)
    #Similar = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = models.Product
        fields = ['name', 'quantity', 'price', 'description', 'front_image', 'rear_image', 'id']

    def get_id(self, obj):
        return obj.pk

    def get_rear_image(self, obj):
        return obj.rear_image.url if obj.rear_image else None

    def get_front_image(self, obj):

        return obj.front_image.url if obj.front_image else None
    
    '''def get_Similar(self, obj):
        
        #print(obj.Categories.all())
        #print()
        
        #similar_products = list(obj.Categories.Product.exclude(id=obj.id))
        
        similar_products = models.Product.objects.filter(Categories__in = [x.id for x in obj.Categories.all()])
        
        #similar_products = ['', '', '', '' '', '']
        
        if len(similar_products) >= 4:
            similar_products = random.sample(list(similar_products), 4)
        
        return similar_products'''


# product review serializer
class ProductReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ProductReview
        fields = ['id', 'stars_count', 'review', 'user', 'product', 'username', 'avatar', 'created', 'is_edited']
        
    def get_username(self, obj):
        
        return obj.user.username
    
    def get_avatar(self, obj):
        return obj.user.userprofile.avatar.url if obj.user.userprofile.avatar else None
    