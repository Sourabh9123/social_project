from account.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.urls import reverse
from django.db.models import Q

from app.models import FriendshipRequest

class SearchUserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name", "last_name",]




class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class ShowFriendRequestSerializer(serializers.ModelSerializer):
    sender = SenderSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ['sender', 'status', 'created_at']


class ShowFriendListSerializer(ModelSerializer):
    friend  = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = FriendshipRequest
        fields = ['friend',]

    def get_friend(self, obj):
        request = self.context.get("request")
        user = request.user
        friends = friends = FriendshipRequest.objects.filter(
        Q(sender=user) | Q(receiver=user),
        status="accepted"
        )
        return friends.first_name






class FriendshipRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = "__all__"