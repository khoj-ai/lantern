from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from user_manager.models import UserMetadata
import uuid

# Serializer to Get User Details using Django Token Authentication
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["id", "username"]

# Serializer to Register New User
class RegisterSerializer(serializers.ModelSerializer):

	email = serializers.EmailField(
		required=True,
		validators=[UniqueValidator(queryset=User.objects.all())]
 	)
  	
	password = serializers.CharField(
		write_only=True, required=True, validators=[validate_password]
	)

	password2 = serializers.CharField(write_only=True, required=True)
  	
	class Meta:
		model = User
		fields = ('password', 'password2', 'email')
		extra_kwargs = {
			'email': {'required': True},
			'password': {'required': True}
		}
	
	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match"})
		
		existing_user = User.objects.filter(email=attrs['email'])
		if existing_user.exists():
			raise serializers.ValidationError({"email": "Email is already in use"})
		
		return attrs
  	
	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['email'],
			email=validated_data['email'],
		)
		
		user.set_password(validated_data['password'])
		user.save()
		UserMetadata.objects.create(user=user, guid=uuid.uuid4())
		return user
