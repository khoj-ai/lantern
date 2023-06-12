from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserInterest, InterestFields
from .serializer import UserInterestSerializer

from django.contrib.auth.models import User

class UserInterestListApiView(APIView):

    def get(self, request):
        user_interests = UserInterest.objects.all()
        serializer = UserInterestSerializer(user_interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'interest' not in data:
            return Response({'error': 'interest is required'}, status=status.HTTP_400_BAD_REQUEST)
        interest = data['interest']
        if interest not in [field[0] for field in InterestFields.choices]:
            return Response({'error': 'interest is invalid'}, status=status.HTTP_400_BAD_REQUEST)

        email = data.get('email', None)
        if email is None:
            return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
        else:
            user = User.objects.create_user(username=email, email=email)

        user_interest = UserInterest.objects.create(user=user, field=interest)
        serializer = UserInterestSerializer(user_interest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
