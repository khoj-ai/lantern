from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import UserInterest
from .serializer import UserInterestSerializer

from django.contrib.auth.models import User
import uuid


class UserInterestListApiView(APIView):
    def post(self, request):
        data = request.data

        email = data.get("email", None)
        if email is None:
            return Response(
                {"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if UserInterest.objects.filter(user=user).exists():
                user_interest = UserInterest.objects.get(user=user)
                serializer = UserInterestSerializer(user_interest)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                user_interest = UserInterest.objects.create(
                    user=user, unique_identifier=uuid.uuid4()
                )
                serializer = UserInterestSerializer(user_interest)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        user = User.objects.create_user(username=email, email=email)

        user_interest = UserInterest.objects.create(
            user=user, unique_identifier=uuid.uuid4()
        )
        serializer = UserInterestSerializer(user_interest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
