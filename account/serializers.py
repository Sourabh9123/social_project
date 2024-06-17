from rest_framework.serializers import ModelSerializer
from account.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields  = "__all__"




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    