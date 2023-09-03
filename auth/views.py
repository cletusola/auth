from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED , HTTP_400_BAD_REQUEST


from .serializers import RegisterSerializer 


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
                status =HTTP_201_CREATED
            )
        else:
            return Response(
                {              
                    "message": "Unable to create account"
                },
                status = HTTP_400_BAD_REQUEST
            )