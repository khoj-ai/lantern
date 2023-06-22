from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import UserInterest
from .serializer import UserInterestSerializer

from django.contrib.auth.models import User
import uuid
from django.http import HttpResponse
from django.contrib.auth.password_validation import validate_password


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


class UserInterestValidApiView(APIView):
    def get(self, request, unique_identifier):
        if not UserInterest.objects.filter(
            unique_identifier=unique_identifier
        ).exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        user_interest = UserInterest.objects.get(unique_identifier=unique_identifier)
        user_interest.waitlist = False
        user = user_interest.user
        if user.has_usable_password():
            return Response({}, status=status.HTTP_410_GONE)
        user_interest.save()
        return Response({"email": user.email}, status=status.HTTP_200_OK)


class InvitedUserSetPassword(APIView):
    def post(self, request, unique_identifier):
        if not UserInterest.objects.filter(
            unique_identifier=unique_identifier
        ).exists():
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        user_interest = UserInterest.objects.get(unique_identifier=unique_identifier)
        user = user_interest.user
        if user.has_usable_password():
            return Response({}, status=status.HTTP_410_GONE)
        data = request.data
        password = data.get("password", None)
        if password is None:
            return Response(
                {"error": "password is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            validate_password(password)
        except Exception as e:
            return Response({"errors": e}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({}, status=status.HTTP_200_OK)
