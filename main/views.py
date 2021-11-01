from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer

from main.models import Coupon, CustomUser, UserProfile
from main.serializers import UserProfileSerializer, UserSerializer, ProfileImagesSerilizer

# get user profile view
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def getUserProfile(request, pk = None):
    try:
        user = CustomUser.objects.get(pk = pk)
        userprofile = UserProfile.objects.get(user=user)
         
        seriliserU = UserProfileSerializer(instance=userprofile)
        
        return Response(seriliserU.data, status = status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response({'error':"User not found."},status = status.HTTP_404_NOT_FOUND)



# update user profile view
@api_view(['PUT', 'PATCH', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def updateUserProfile(request, pk = None):
    try:
        data = request.data

        if data:
            user = CustomUser.objects.get(pk = pk)
            userprofile = user.userprofile
         
            seriliserU = UserProfileSerializer(instance=userprofile, data=data, partial = True)
        
            if seriliserU.is_valid():
                s = seriliserU.save()
        
                return Response(s.data, status = status.HTTP_200_OK)

        return Response({'error':'Could not edit profile.'}, status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        return Response({'error':"User not found."},status = status.HTTP_404_NOT_FOUND)


# get user view
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated])
def getUser(request, pk = None):
    try:
        user = CustomUser.objects.get(pk = pk)
        seriliserU = UserSerializer(user, many=False)

        return Response(seriliserU.data, status = status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found.'},status = status.HTTP_404_NOT_FOUND)


# update the header and avatar image
@api_view(['PUT', 'PATCH', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAdminUser])
def profileImages(request):

    user = request.user
    data = request.data

    if data:
        
        serializer = ProfileImagesSerilizer(instance = user.userprofile, data = data, partial = True)

        if(serializer.is_valid()):
            updated_pic_url = serializer.save()

            header = updated_pic_url.HeaderImage.url if updated_pic_url.HeaderImage else None
            avatar = updated_pic_url.Avatar.url if updated_pic_url.Avatar else None

            return Response({'HeaderImage': header, 'Avatar': avatar}, status=status.HTTP_200_OK)

    return Response({'error': 'Could not update profile images'}, status=status.HTTP_400_BAD_REQUEST)



# get coupon amount by code.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny])
def getCouponAmount(request, code=None):

    try:

        coupon = Coupon.objects.get(Code = code , isValid = True)
        return Response({'amount': coupon.amount}, status=status.HTTP_200_OK)

    except Coupon.DoesNotExist:
        return Response({'error': 'Coupon code not valid.'}, status=status.HTTP_400_BAD_REQUEST)
