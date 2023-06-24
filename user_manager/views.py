from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from rest_framework import status


# Class based view to get user details using Django Token Authentication
class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CheckValidCredentials(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return Response({}, status=status.HTTP_200_OK)
        data = request.data
        username = data.get("email", None)
        password = data.get("password", None)
        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password"},
                status=400,
            )
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_404_NOT_FOUND
            )
        login(request, user)
        return Response({}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"message": "User Logged Out Successfully"})


# Class based view to register new user
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
