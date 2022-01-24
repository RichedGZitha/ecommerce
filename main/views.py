import os
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import Coupon, CustomUser, UserProfile
from main.serializers import UserProfileSerializer, UserSerializer, ProfileImagesSerilizer


# verify email upon registration.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def activateUser(request, uid = None, token = None):
        payload = {'uid': uid, 'token': token}

        url = "http://127.0.0.1:8000/auth/v1/users/activation/"
        response = requests.post(url, data = payload)
        
        context = {'title': 'Activation complete', 'heading':'Account activation successful', 
        'message':'Thank you for creating an account with us. Feel free to contact us should you encounter any issues.', 
        'redirect': settings.FRONTEND_URL, 'action':'Sign in'}

        if response.status_code == 204:
            #return Response({}, response.status_code)
            return render(request,'main/auth/activationConfirmation.html', context)
        else:
            return HttpResponse(memoryview(b'Something went wrong. Please try again'))
            #return render(request,'main/auth/activationConfirmation.html', context)
            #return Response(response.json())

            
''' confirm username reset.
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def usernameReestConfirm(request, uid = None, token=None):
        
        redirect = 'http://127.0.0.1:3000'
        baseURL  = 'http://127.0.0.1:8000'

        if request.method == 'POST':
        
            username = request.POST.get('username')
            confirm_username = request.POST.get('confirmusername')
               
            if username != confirm_username:
                context = {'errors': ['Username do not match.'], 'redirect':redirect, 'uid':uid, 'token':token}
                
                return render(request,'main/auth/passwordResetConfirmation.html', context)
            
            payload = {'uid': uid, 'token': token, 'new_password':username}

            url = baseURL + "/auth/v1/users/reset_password_confirm/"
            response = requests.post(url, data = payload)

            # password reset complete.
            if response.status_code == 204:
                
                return redirect(reverse('username-reset-successful'))
            else:
                #return Response(response.json())
                return HttpResponse(memoryview(b'Something went wrong please try to reset the username again from the begining.'))
                
        else:
            context = {'redirect':redirect, 'uid':uid, 'token':token}
            return render(request,'main/auth/passwordResetConfirmation.html', context)
            
'''            

# confirm password reset.
@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def passwordReestConfirm(request, uid = None, token=None):
        
        redirect = settings.FRONTEND_URL
        baseURL  = 'http://127.0.0.1:8000'

        if request.method == 'POST':
        
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmpassword')
               
            if password != confirm_password:
                context = {'errors': ['Passwords do not match.'], 'redirect':redirect, 'uid':uid, 'token':token}
                
                return render(request,'main/auth/passwordResetConfirmation.html', context)
            
            payload = {'uid': uid, 'token': token, 'new_password':password}

            url = baseURL + "/auth/v1/users/reset_password_confirm/"
            response = requests.post(url, data = payload)

            # password reset complete.
            if response.status_code == 204:
                
                return redirect(reverse('password-reset-successful'))
            else:
                #return Response(response.json())
                return HttpResponse(memoryview(b'Something went wrong please try to reset the password again from the begining.'))
                
        else:
            context = {'redirect':redirect, 'uid':uid, 'token':token}
            return render(request,'main/auth/passwordResetConfirmation.html', context)
            
            
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def passwordResetSuccessful(request):
        
        context = {'title': 'Password Reset complete', 'heading':'Password Reset successful', 
        'message':'Your password was successfuly reset. Feel free to contact us should you encounter any issues.', 
        'redirect':settings.FRONTEND_URL, 'action':'Sign in'}

        
        return render(request,'main/auth/passwordResetSuccessful.html', context)
                

# generates a csrf token
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,])
def getCSRFTokenView(request):
    csrf_token = get_token(request)
    
    return Response({'csrf': csrf_token}, status = status.HTTP_200_OK)


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
        
        
# get user profile view
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])
def getMyProfile(request):
    try:
        user = CustomUser.objects.get(pk = request.user.pk)
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

            header = updated_pic_url.header_image.url if updated_pic_url.header_image else None
            avatar = updated_pic_url.avatar.url if updated_pic_url.avatar else None

            return Response({'header_image': header, 'avatar': avatar}, status=status.HTTP_200_OK)

    return Response({'error': 'Could not update profile images'}, status=status.HTTP_400_BAD_REQUEST)



# get coupon amount by code.
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny])
def getCouponAmount(request, code=None):

    try:

        coupon = Coupon.objects.get(code = code , isValid = True)
        return Response({'amount': coupon.amount}, status=status.HTTP_200_OK)

    except Coupon.DoesNotExist:
        return Response({'error': 'Coupon code not valid.'}, status=status.HTTP_400_BAD_REQUEST)
        

# get the shipment information of the user for checkout.    
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,]) 
def GetShipmentAdressView(request):
    
    profile = request.user.userprofile
    data = dict()
    
    data["phone"] = profile.contact_number
    data["email"] = request.user.email
    data["country"] = profile.country
    data["street_address"] = profile.street_address
    data["city"] = profile.city
    data["postal_code"] = profile.postal_code
    data["suburb"] = profile.suburb
    data["province"] = profile.province
    
    return Response(data, status=status.HTTP_200_OK)


# logout of all devices.
@api_view(['POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,]) 
def LogoutAllAPIView(request):
    
    tokens = OutstandingToken.objects.filter(user_id=request.user.id)
    for token in tokens:
        t, _ = BlacklistedToken.objects.get_or_create(token=token)

    return Response(status=status.HTTP_205_RESET_CONTENT)
    

# logout from single device.
@api_view(['POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.IsAuthenticated,])  
def LogoutAPIView(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# allow user to login using email and password.
@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
@permission_classes([permissions.AllowAny,]) 
def LoginView(request):
    
    context = dict()
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        next_ = request.POST["next"]
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_)
            
        else:
            # Return an 'invalid login' error message.
            context["next"] = next_
            context["errors"] = ["Email or Password is incorrect please try again."]
            return render(request,'main/auth/login.html', context)
        
    next_ = request.GET.get("next")
    context["next"] = next_
    
    return render(request,'main/auth/login.html', context)
    
 
# logout using without api.
def LogoutView(request):
    logout(request)
    next_ = request.GET.get("next")
    return HttpResponseRedirect(next_ if next_ else settings.FRONTEND_URL)
 