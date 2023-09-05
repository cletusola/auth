from django.contrib.auth import authenticate 

from rest_framework import generics, status 
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework_simplejwt.tokens import RefreshToken 

from .serializers import RegisterSerializer, LoginSerializer


""" Registration view """ 
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            return Response(
                {
                    "message":"Account created",
                    "user":user.username
                },
                status = status.HTTP_201_CREATED
            )
        else:
            return Response(
                {              
                    "message": "Unable to create account"
                },
                status = status.HTTP_400_BAD_REQUEST
            )


""" Login View """ 
class LoginView(APIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user is not None:
                
                if user.is_active:
                    
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    return Response({
                        "access_token": access_token
                        },
                        status = status.HTTP_200_OK
                    )
                else:

                    return Response({
                        "message":"Your account is inactive, please contact our support"
                        },
                        status = status.HTTP_401_UNAUTHORIZED
                    )
            else:
                
                return Response({
                    "message":"Incorrect username or password"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )



""" Logout view """ 
class LogoutView(APIView):

    def post(self, request, *args, **kwargs):

        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

            except Exception as e:
                pass 

        return Response(status = status.HTTP_204_NO_CONTENT)
