from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics


# Class based view to get user details using Django Token Authentication
class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# Class based view to register new user
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
