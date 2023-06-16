from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .models import UserInterest, InterestFields
from .serializer import UserInterestSerializer

from django.contrib.auth.models import User
import uuid


class UserInterestListApiView(generics.CreateAPIView):
    def post(self, request):
        data = request.data

        if "interest" not in data:
            return Response(
                {"error": "interest is required"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        interest = data["interest"]
        if interest not in [field[0] for field in InterestFields.choices]:
            return Response(
                {"error": "interest is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type="application/json",
            )

        email = data.get("email", None)
        if email is None:
            return Response(
                {"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            existing_interest = UserInterest.objects.filter(user=user)
            if existing_interest.exists():
                existing_interest = existing_interest.get()
                existing_interest.field = interest
                if existing_interest.unique_identifier is None:
                    existing_interest.unique_identifier = uuid.uuid4()
                existing_interest.save()
                serializer = UserInterestSerializer(existing_interest)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.create_user(username=email, email=email)

        user_interest = UserInterest.objects.create(
            user=user, field=interest, unique_identifier=uuid.uuid4()
        )
        serializer = UserInterestSerializer(user_interest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
