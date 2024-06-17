from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from account.serializers import LoginSerializer, UserSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from account.models import User
from django.contrib.auth import authenticate, login, logout 
from rest_framework.permissions import IsAuthenticated




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }





def populate_users(n):
    for i in range(n):
            user = User.objects.create(
                first_name = "sourabh",
                last_name ="last_name",
                email = f"sourabhd{i}@gmail.com",
                password = make_password("9038")
            )
    return "populated users"
     



    



class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        if "email" in request.data:
            request.data['email'] = request.data['email'].lower()
        else:
            return Response({"error":"please provide Email"})
        
        serializer = UserSerializer(data=request.data)
      
        if serializer.is_valid():
            
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            user = User.objects.get(email=serializer.validated_data["email"])
            token = get_tokens_for_user(user)
            return Response({"response":"account created",'token':token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class LogInview(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer  = LoginSerializer(data=request.data)
        email = request.data['email'].lower()
        is_user = User.objects.filter(email=email).exists()


        
        try:
            if serializer .is_valid():
                email = email
                password = serializer.validated_data['password']
                user= authenticate(request, username=email, password=password)
                login(request, user)
             
                token = get_tokens_for_user(user)
        
                response_data = {
                    'token' :  token,
                }
               
                
                return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:

            if is_user:
                return Response({'message':'password does not match'},status=status.HTTP_400_BAD_REQUEST )
            return Response({'message':'user does not exist'},status=status.HTTP_400_BAD_REQUEST )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
