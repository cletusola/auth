from rest_framework import serializers 
from django.contrib.auth import get_user_model

User = get_user_model()




""" Register serializer """ 
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=4, max_length=20, required=True)
    email = serializers.EmailField(min_length=8, max_length=80, required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = User 
        fields = ('username','email','password')


    def create(self, validated_data):

        username = validated_data['username']
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return user 


""" Login serializer """ 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=4, max_length=20, required=True)
    password = serializers.CharField(min_length=8, required=True)