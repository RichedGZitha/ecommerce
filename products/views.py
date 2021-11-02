from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, generics
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from main import serializers

from products.models import Category, Product, ProductReview
from products.serializers import CategorySerializer, ProductDisplaySerializer, ProductManagerSerializer, ProductReviewSerializer


# TODO Check if person is manager or merchant.
# TODO Use single to: Call async to send email to those responsible for the product of this change. Async!!
# create product
class CreateProduct(generics.CreateAPIView):
    serializer_class = ProductManagerSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# create  product review
# TODO: Call async to send email to those responsible for the product that a new review was created. Async!!
class CreateProductReview(generics.CreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# get and edit product
@api_view(['PUT', 'PATCH', 'GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def editOrGetProductsManager(request, pk = None):

    # check if user is manager or merchant.
    user = request.user
    if user.groups.filter(Q(name = 'Merchant') | Q(name = 'Manager')).exists() == False:
        return Response({'error':'Not allowed'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':

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

    else:

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


# useed for display single product
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny])
def getProductForDisplay(request, pk = None):

    try:

        product = Product.objects.get(pk = pk)
        pSerializer = ProductDisplaySerializer(instance=product)

        return Response(pSerializer.data, status = status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'error':'Product not found.'},status=status.HTTP_404_NOT_FOUND)


# get the first 500 products
# get based on query 
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny])
def getProductsQuery(request):

    q = request.GET.get('q')
    categoryQ = request.GET.get('category')

    products = None

    # filter by name and description
    # later on Brand, Manufacturer, location

    if q:
        products = Product.objects.filter(Q(Name__contains = q) | Q(Description__contains = q) | Q(isActive = True))[:200]
    else:
        products = Product.objects.filter(isActive = True).all()[:200]

    # filter by category.
    if categoryQ:

        category = Category.objects.filter(Name__contains = categoryQ).first()
        prodArray = []

        for prod in products:

            if category in prod.categories:
                prodArray.append(prod)

        # only add if there is match.
        if len(prodArray) > 0:
            products = prodArray


    # filter by price range.
    max_priceQ = request.GET.get('max_price')
    min_priceQ = request.GET.get('min_price')

    if max_priceQ and min_priceQ:

        try:
            max_price = int(max_priceQ)
            min_price = int(min_priceQ)

            products = products.filter(Price__range=(min_price, max_price))
        except (TypeError, ValueError, OverflowError, ArithmeticError, FloatingPointError,):
            pass
    
    productSerializer = ProductDisplaySerializer(products, many=True)
    return Response(productSerializer.data, status=status.HTTP_200_OK)


# get categories for a particular product.
# only managers and merchants should access this view.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def getProductcategories(request, pk = None):

    # if user is manager or merchant.
    user = request.user
    if user.groups.filter(Q(name = 'Merchant') | Q(name = 'Manager')).exists() == False:
        return Response({'error':'Not allowed'}, status=status.HTTP_401_UNAUTHORIZED)
    
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
@api_view(['POST', 'PUT', 'PATCH'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
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
                revS = ProductReviewSerializer(instance =review, many = False, data=data)

                if revS.is_valid():
                    # update data on database.
                    revSSaved = revS.save()

                    # TODO: Call async to send email/create notification to those responsible for the product of this change/edit. Async!!

                    return Response(revSSaved.data, status=status.HTTP_200_OK)
    
        except ProductReview.DoesNotExist:
            return Response({'error':' Product review not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error':'Could not edit the product review'}, status=status.HTTP_400_BAD_REQUEST)


# update the categories of a products
@api_view(['PUT', 'PATCH', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def updateProductCategories(request, pk = None):

    # check if user is manager or merchant.
    user = request.user
    if user.groups.filter(Q(name = 'Merchant') | Q(name = 'Manager')).exists() == False:
        return Response({'error':'Not allowed'}, status=status.HTTP_401_UNAUTHORIZED)

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
            cat_obj_list = [Category.objects.get_or_create(Name = category)[0] for category in cat_list]

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
                catObj = Category.objects.filter(Name = cat).first()

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