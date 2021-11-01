from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, generics
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from main import serializers

from products.models import Category, Product, ProductReview
from products.serializers import CategorySerializer, ProductDisplaySerializer, ProductManagerSerializer, ProductReviewSerializer


# create product
class CreateProduct(generics.CreateAPIView):
    serializer_class = ProductManagerSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


# create  product review
class CreateProductReview(generics.CreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

# get and edit product
@api_view(['PUT', 'PATCH', 'GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def productView(request, pk = None):

    # if the user is not a manager.
    if request.user.userprofile.isManager != True:
        return Response({'error':'Not Allowed.'},status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':

        try:
            product = Product.objects.get(pk = pk)
            productSerializer = ProductManagerSerializer(instance=product)
            return Response(productSerializer.data, status =status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    else:

        data = request.data

        if not data:
            return Response({'error':'Could not update the product.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk = pk)

            productSerializer = ProductManagerSerializer(data=data, partial = True, instance=product)
        
            if productSerializer.is_valid():
                productSSaved = productSerializer.save()

                return Response(productSSaved.data, status =status.HTTP_200_OK)

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
# only managers should access this view.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def getProductcategories(request, pk = None):

    if request.user.userprofile.isManager != True:
        return Response({'error':'Not allowed.'},status=status.HTTP_401_UNAUTHORIZED)

    try:
        categories = Product.objects.get(pk = pk).Categories

        catSerializer = CategorySerializer(categories, many=True)

        return Response(catSerializer.data, status=status.HTTP_200_OK)

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



# update the categories of a products
@api_view(['PUT', 'PATCH', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def updateProductCategories(request, pk = None):

    data = request.data.get('categories')

    if not data or '#' not in data:
        return Response({'error': 'Please provide # separated values.'}, status = status.HTTP_400_BAD_REQUEST)

    # covert comma separated string into an array.
    cat_list = data.split('#')

    # get or instantiate categories instances.
    cat_obj_list = [Category.objects.get_or_create(Name = category)[0] for category in cat_list]

    try:
         # set to list of categories.
        product = Product.objects.get(pk = pk)
        product.Categories.set(cat_obj_list)

        p = product.save()

        serializer = ProductManagerSerializer(p, many = False)
        return Response(serializer.data, status = status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response({'error':'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
