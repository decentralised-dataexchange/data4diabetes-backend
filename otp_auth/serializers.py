from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegisterUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=17)
    firstname = serializers.CharField(max_length=20)
    lastname = serializers.CharField(max_length=20)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        User = get_user_model()
        user = User(username=validated_data.get("mobile_number"),
                    mobile_number=validated_data.get("mobile_number"),
                    firstname=validated_data.get("firstname"),
                    lastname=validated_data.get("lastname"))
        user.set_unusable_password()
        user.save()
        return user
    
class LoginUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=17)