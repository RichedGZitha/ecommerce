import random
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, generics
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema 
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from products.models import Category, Product, ProductReview
from products.serializers import CategorySerializer, ProductDisplaySerializer, ProductManagerSerializer, ProductReviewSerializer
from . import utils

# TODO Check if person is manager or merchant.
# TODO Use single to: Call async to send email to those responsible for the product of this change. Async!!
# create product

class CreateProduct(generics.CreateAPIView):
    serializer_class = ProductManagerSerializer
    permission_classes = [permissions.IsAuthenticated, utils.IsManager, utils.IsMerchant]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# create  product review
# TODO: Call async to send email to those responsible for the product that a new review was created. Async!!

class CreateProductReview(generics.CreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# get and edit product
@swagger_auto_schema(methods=['put', 'patch'], 
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, # object because the data is in json format
    properties={
        'name':openapi.Schema(type=openapi.TYPE_STRING, description = 'Name of the product.'),
        'quantity':openapi.Schema(type=openapi.TYPE_NUMBER, description = 'Quantity of products left.'),
        'price':openapi.Schema(type=openapi.TYPE_NUMBER, description = 'Price of the product.'),
        'is_special':openapi.Schema(type=openapi.TYPE_BOOLEAN, description = 'Indicates whether the product is on special.'),
        'is_active':openapi.Schema(type=openapi.TYPE_BOOLEAN, description = 'Indicates whether the product is active.'),
        'description':openapi.Schema(type=openapi.TYPE_STRING, description = 'Description of the product.')
    },

    required = []
    
), operation_id="editproductreview_view_id")
@api_view(['PUT', 'PATCH'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated, utils.IsManager, utils.IsMerchant])
def editProductsManager(request, pk = None):

    # check if user is manager or merchant.
    user = request.user
    data = request.data
    
    if not data:
        return Response({'error':'Could not update the product.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = None

        # if manager.
        if user.groups.filter(name = 'Manager').exist():
            product = Product.objects.get(pk = pk)
        elif user.groups.filter(name = 'Merchant').exist():
            # To prevent subbotaging the competitor's products.
            product = Product.objects.get(pk = pk, managerOrMerchant = user)

        # if product was found.
        if product:
            productSerializer = ProductManagerSerializer(data=data, partial = True, instance=product)
        
            # if provided data is valid product data. 
            if productSerializer.is_valid():
                productSSaved = productSerializer.save()

                # TODO: Call async to send email to those responsible for the product of this change. Async!!

                return Response(productSSaved.data, status =status.HTTP_200_OK)
            else:
                return Response({'error':'Could not edit the product.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # merchant does not have permission to edit this product: Competitors product.
        else:
            return Response({'error':'Not allowed to view this product.'}, status=status.HTTP_401_UNAUTHORIZED)

    except Product.DoesNotExist:
        return Response({'error':'Product not found.'}, status=status.HTTP_404_NOT_FOUND)


# get product
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, utils.IsManager, utils.IsMerchant])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def getProductAdmin(request, pk):

    user = request.user

    try:
        product = None

        # if manager.
        if user.groups.filter(name = 'Manager').exist():
            product = Product.objects.get(pk = pk)
        elif user.groups.filter(name = 'Merchant').exist():
            # To prevent subbotaging the competitor's products.
            product = Product.objects.get(pk = pk, managerOrMerchant = user)
            
        # if product was found.
        if product:
            productSerializer = ProductManagerSerializer(instance=product)
            return Response(productSerializer.data, status =status.HTTP_200_OK)
        else:
            return Response({'error':'Not allowed to view this product.'}, status=status.HTTP_401_UNAUTHORIZED)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)


# useed for display single product
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny])
def getProductForDisplay(request, pk = None):

    try:

        product = Product.objects.get(pk = pk)
        pSerializer = ProductDisplaySerializer(instance=product)
        
        similar_products = Product.objects.filter(categories__in = [x.id for x in product.categories.all()]).exclude(pk = product.pk).distinct()
        
        if len(similar_products) >= 4:
            similar_products = random.sample(list(similar_products), 4)
        
        data = pSerializer.data
        data["similar"] = [{'id':x.id, 'name':x.name, 'front_image':x.front_image.url if x.front_image else None, 'price': x.Price, 'description': x.description} for x in similar_products]
        
        return Response(data, status = status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'error':'Product not found.'},status=status.HTTP_404_NOT_FOUND)


# get the first n products
# get based on query 
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
#@permission_classes([permissions.AllowAny])
def getProductsQuery(request):

    q = request.GET.get('q')
    n = int(request.GET.get('count') if request.GET.get('count') else 200)
    categoryQ = request.GET.get('category')
    special = request.GET.get('special')
    featured = request.GET.get('featured')

    products = None

    # filter by name and description
    # later on Brand, Manufacturer, location

    if q:
        products = Product.objects.filter(Q(name__contains = q) | Q(description__contains = q) | Q(is_active = True))
    else:
        products = Product.objects.filter(is_active = True)
        
        
    # TODO: filter based on product special
    if special == "yes":
        products = products.filter(Q(is_special = True))
    
    # TODO: Filter based on category special
    if featured == "true":
        products = products.filter(is_featured = True)
    
    # TODO: filter based on royalty points.
    
    # TODO: Filter based on membership discount.
    
    # filter by price range.
    max_priceQ = request.GET.get('max_price')
    min_priceQ = request.GET.get('min_price')

    if max_priceQ and min_priceQ:

        try:
            max_price = int(max_priceQ)
            min_price = int(min_priceQ)

            products = products.filter(price__range=(min_price, max_price))
        except (TypeError, ValueError, OverflowError, ArithmeticError, FloatingPointError,):
            pass

    # TODO: filter by category.
    if categoryQ:

        category = Category.objects.filter(name__contains = categoryQ).first()
        prodArray = []

        for prod in products:

            if category in prod.categories:
                prodArray.append(prod)

        # only add if there is match.
        if len(prodArray) > 0:
            products = prodArray

    productSerializer = ProductDisplaySerializer(products[:n], many=True)
    return Response(productSerializer.data, status=status.HTTP_200_OK)


# get categories for a particular product.
# only managers and merchants should access this view.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def getProductcategories(request, pk = None):

    # if user is manager or merchant.
    user = request.user
    
    try:
        categories = None

        if user.groups.filter(name = 'Manager').exists():
            categories = Product.objects.get(pk = pk).Categories
        elif user.groups.filter(name = 'Merchant').exists():
            # this must have been created by them.
            categories = Product.objects.get(pk = pk, managerOrMerchant = user).Categories

        # if category was found.
        if categories:
            catSerializer = CategorySerializer(categories, many=True)
            return Response(catSerializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Not allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    except Product.DoesNotExist:

        return Response({'error':'Product not found.'},status=status.HTTP_404_NOT_FOUND)


# get product reviews
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def getProductReviews(request, pk = None):
    
    # we are getting alist of reviews no need to use try-except
    reviews = ProductReview.objects.filter(product = pk)
    revS = ProductReviewSerializer(reviews, many = True)

    return Response(revS.data, status=status.HTTP_200_OK)


# get all available categories.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def getAllCategories(request):
    
    # we are getting alist of reviews no need to use try-except
    categories = Category.objects.all()
    catSerializer = CategorySerializer(categories, many = True)

    return Response(catSerializer.data, status=status.HTTP_200_OK)





# get product reviews
@swagger_auto_schema(methods=['post', 'put', 'patch'], 
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, # object because the data is in json format
    properties={
        'review':openapi.Schema(type=openapi.TYPE_STRING, description = 'The product review message'),
        'stars_count': openapi.Schema(type=openapi.TYPE_NUMBER, description = 'The number of stars given to the product.'),
    },
    
), operation_id="editproductreview_view_id")
@api_view(['POST', 'PUT', 'PATCH'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated])
def editProductReviews(request, pk = None):
    
    data = request.data
    user = request.user

    # if data was provided.
    if data:
        
        try:
            # get the review from database.
            # also use the user attribute to ensure that only the person who made the review, merchant and manager can access this review. 
            review = None

            # check if the user is a merchant or manager.
            if user.groups.filter(Q(name = 'Merchant') | Q(name = 'Manager')).exists():

                # no need to check user, since it may not match.
                review = ProductReview.objects.get(pk = pk)
            else:
                review = ProductReview.objects.get(pk = pk, user = user)

            # if review is in the database.
            if review:
                
                data['is_edited'] = True
                revS = ProductReviewSerializer(instance =review, many = False, data=data, partial=True)

                if revS.is_valid():
                    # update data on database.
                    revS.save()
                   
                    # TODO: Call async to send email/create notification to those responsible for the product of this change/edit. Async!!

                    return Response(revS.data, status=status.HTTP_200_OK)
    
        except ProductReview.DoesNotExist:
            return Response({'error':' Product review not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error':'Could not edit the product review'}, status=status.HTTP_400_BAD_REQUEST)


# update the categories of a products
@swagger_auto_schema(methods=['post', 'put', 'patch'], 
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, # object because the data is in json format
    properties={
        'categories': openapi.Schema(type=openapi.TYPE_STRING, description='This is a string of category names. Separated by #'),
    },
    
), operation_id="updatecategories_view_id")
@api_view(['PUT', 'PATCH', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated, utils.IsManager, utils.IsMerchant])
def updateProductCategories(request, pk = None):

    # check if user is manager or merchant.
    user = request.user
    
    data = request.data.get('categories')

    if not data or '#' not in data:
        return Response({'error': 'Please provide # separated values.'}, status = status.HTTP_400_BAD_REQUEST)

    # convert comma separated string into an array.
    cat_list = data.split('#')

    try:

        # if person is manager.
        if user.groups.filter(name = 'Manager').exists():
            product = Product.objects.get(pk = pk)

            # can create or get a categories.
            cat_obj_list = [Category.objects.get_or_create(Name = category.strip())[0] for category in cat_list]

            # set to list of categories.
            product.Categories.set(cat_obj_list)
            p = product.save()

            serializer = ProductManagerSerializer(p, many = False)

            # TODO: Use async to send email, about this change to merchants responsible for this product. use async !!

            return Response({'rejected': False, 'data': {'product': serializer.data}}, status = status.HTTP_200_OK)

        # merchant editing their own product.
        elif user.groups.filter(name = 'Merchant').exists():
            product = Product.objects.get(pk = pk, managerOrMerchant = user)

            cat_obj_list = []

            # list of rejected category names.
            cat_rejected = []

            for cat in cat_list:
                catObj = Category.objects.filter(name = cat.strip()).first()

                if catObj:
                    cat_obj_list.append(catObj)
                else:
                    # if category is not found in the database.
                    cat_rejected.append(cat)
            

            # all the categories are incorrect.
            if cat_obj_list:

                # set to list of categories
                product.Categories.set(cat_obj_list)
                p = product.save()

                serializer = ProductManagerSerializer(p, many = False)

                # TODO: Use async to send email, about this change to merchants responsible for this product. use async !!

                if len(cat_rejected) > 0:
                    return Response({'rejected': True, 'data': {'product': serializer.data, 'rejected_categories': cat_rejected, 'description': 'You are not allowed to create new categories.'}}, status = status.HTTP_200_OK)

                return Response({'rejected': False, 'data': {'product': serializer.data}}, status = status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'error':'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Could not edit product categories'}, status=status.HTTP_400_BAD_REQUEST)