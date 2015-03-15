from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
	mobile_number = serializers.CharField(required=False, allow_null=True, max_length=10)

	class Meta:
		model = User
		fields = ('mobile_number')