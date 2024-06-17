from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from account.models import User
from account.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import filters
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from app.serializers import (SearchUserSerializers, FriendshipRequestSerializer, ShowFriendRequestSerializer,
                             ShowFriendListSerializer,
                             )
from app.models import FriendshipRequest
import json
from django.core.serializers import serialize
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404


User = get_user_model()




class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SearchUserView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        query = self.request.query_params.get('query', None)

        
        if query:
            if "@" in query or "." in query:
                users = User.objects.filter(email=query.lower())
                return users

            search_terms = query.lower().split()
            q_objects = Q()
            for term in search_terms:
                q_objects |= Q(first_name__icontains=term) | Q(last_name__icontains=term)
            return User.objects.filter(q_objects)
        return User.objects.none()
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = SearchUserSerializers(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)







class SendFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer

    def post(self, request, *args , **kwargs):

        try:

            sender = request.user
            receiver_id = request.data.get("user_id", None)
            if not receiver_id:
                return Response({"error":"please provide user_id"}, status=status.HTTP_400_BAD_REQUEST)
            receiver = get_object_or_404(User, id=receiver_id)
            if receiver == sender:
                return Response({"error": "You can't send request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
            
            if FriendshipRequest.objects.filter(sender=sender, receiver=receiver).exists():
                return Response({"error": "Friendship request already sent."}, status=status.HTTP_400_BAD_REQUEST)
            
            if FriendshipRequest.objects.filter(receiver=sender, sender=receiver).exists():
                is_friend = FriendshipRequest.objects.filter(receiver=sender, sender=receiver).first()
                if is_friend.status == "accepted":
                    return Response({"message": "Already friend."}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "other person sent you request already please check your request section and accept it"}, status=status.HTTP_400_BAD_REQUEST)
        
            one_minute_ago = timezone.now() - timedelta(minutes=1)
            request_count = FriendshipRequest.objects.filter(sender=sender, created_at__gte=one_minute_ago).count()
            if request_count >= 3:
                return Response({"error": "You can only send 3 requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            FriendshipRequest.objects.create(sender=sender, receiver=receiver)
            return Response({"message": "Friendship request sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


            





class FriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendshipRequest.objects.all()
    

    def get(self, request, *args, **kwargs):

        pending_requests = FriendshipRequest.objects.filter(receiver=request.user, status="pending")
        serializer = ShowFriendRequestSerializer(pending_requests, many=True)
        return Response({"friend_requests": serializer.data}, status=status.HTTP_200_OK)
    


class AcceptFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer
   
    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id", None)
        if not user_id:
            return Response({"error":"please provide user_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except Exception  as e:
            return  Response({"error": "User associated with this ID does not exist"},status=status.HTTP_400_BAD_REQUEST)
        is_request = FriendshipRequest.objects.filter(sender=user, receiver=request.user).exists()

   
        if is_request:
            already_accepted = FriendshipRequest.objects.filter(sender=user, receiver=request.user, status="accepted")
            if already_accepted:
                return Response({"error":"Friend Request Already accepted"}, status=status.HTTP_400_BAD_REQUEST)

            is_request = FriendshipRequest.objects.filter(sender=user, receiver=request.user).first()
     
            is_request.status="accepted"
            is_request.save()
            return Response({"message":"Request Accepted"}, status=status.HTTP_200_OK)
        else:
            return  Response({"error": "You did not get request from this user"},status=status.HTTP_400_BAD_REQUEST)







class RejectFriendRequestView(GenericAPIView):
    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):  
        try:

            user_id = request.data.get("user_id", None)
            if user_id:
                user = get_object_or_404(User, id=user_id)
                is_request = FriendshipRequest.objects.filter(sender=user, receiver=request.user).exists()
                
                if is_request:
                    already_rejected =  FriendshipRequest.objects.filter(sender=user, receiver=request.user,status="rejected")
                    if already_rejected:
                        return Response({"error":"You have Already rejected this User's request"}, status=status.HTTP_200_OK)

                    is_request = is_request = FriendshipRequest.objects.filter(sender=user, receiver=request.user).first()
                    is_request.status="rejected"
                    is_request.save()
                    return Response({"message":"Request Rejected"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":"you did not get request from this user"}, status=status.HTTP_200_OK)
            else:
                return Response({"error":"please provide user_id"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetMyAllFriendView(GenericAPIView):
    queryset = FriendshipRequest.objects.all()
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, *args, **kwargs):
        user = request.user 
        friends = FriendshipRequest.objects.filter(
            Q(sender=user) | Q(receiver=user),
            status="accepted"
            ).select_related('sender', 'receiver')
        if not friends:
            return Response({"my_friends":[]}, status=status.HTTP_200_OK)
        my_friends = []
        for friend in friends:
            if friend.sender == user:
                unique_id = friend.receiver.id
                first_name = friend.receiver.first_name
                last_name = friend.receiver.last_name
                email =  friend.receiver.email
            else:
                first_name = friend.sender.first_name
                last_name = friend.sender.last_name
                email =  friend.sender.email
                unique_id = friend.sender.id


            
            result = {
                "unique_id":unique_id ,
                "email" : email,
                "first_name":first_name,
                "last_name" : last_name,          
            }
            my_friends.append(result)

        return Response({"my_friends":my_friends}, status=status.HTTP_200_OK)
    




