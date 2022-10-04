from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserLoginSerializer,UserRegistrationSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UseRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# generate  token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
  renderer_classes =[UseRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token=get_tokens_for_user(user)
    return Response({'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes =[UseRenderer]
  def post(self, request, format=None):
    serializer =UserLoginSerializer(data=request.data)
   
    if  serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
    if user != None:
      token =get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login sucessfull!'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes =[UseRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request,format=None):
    serializer=UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes =[UseRenderer]
    permission_classes = (IsAuthenticated,)
    def post(self,request,formate=None):
      serializer= UserChangePasswordSerializer(data=request.data, context={'user':request.user})
      if  serializer.is_valid(raise_exception=True):
        return Response({'msg':'password change sucessfull!'}, status=status.HTTP_200_OK)
      else:
        return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
class SendPasswordResetEmailView(APIView):
  renderer_classes =[UseRenderer]
  def post(self, request, formate=None):
    serializer=SendPasswordResetEmailSerializer(data=request.data)
    if  serializer.is_valid(raise_exception=True):
      return Response({'msg':'password reset link send. please check your email!'}, status=status.HTTP_200_OK)
class UserPasswordResetView(APIView):
  renderer_classes =[UseRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
