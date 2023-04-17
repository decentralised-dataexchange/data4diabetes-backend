from django.test import TestCase
from rest_framework import serializers
from django.contrib.auth import get_user_model
from otp_auth.serializers import RegisterUserSerializer
from otp_auth.user import get_user_by_mobile_number, is_user_active

class RegisterUserSerializerTestCase(TestCase):
    def test_register_user_serializer(self):
        """Test register user serializer"""
        data = {'mobile_number': '+91000000',
                'firstname': 'John', 'lastname': 'Doe'}
        serializer = RegisterUserSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        validated_data = serializer.validated_data
        self.assertEqual(validated_data['mobile_number'], '+91000000')
        self.assertEqual(validated_data['firstname'], 'John')
        self.assertEqual(validated_data['lastname'], 'Doe')

    def test_create_user_from_serializer(self):
        """Test create user from serializer"""
        data = {'mobile_number': '+91000000',
                'firstname': 'John', 'lastname': 'Doe'}
        serializer = RegisterUserSerializer(data=data)

        self.assertTrue(serializer.is_valid())

        serializer.save()

        User = get_user_model()
        user = User.objects.get(username="+91000000")
        self.assertEqual(user.mobile_number, "+91000000")
        self.assertEqual(user.firstname, "John")
        self.assertEqual(user.lastname, "Doe")
        self.assertFalse(user.has_usable_password())

    def test_get_user_by_mobile_number(self):
        """Test get user by mobile number"""
        User = get_user_model()
        user = User(username="+91000000", 
                    mobile_number="+91000000", 
                    firstname="John", 
                    lastname="Doe")
        user.set_unusable_password()
        user.save()

        user, is_user_exists = get_user_by_mobile_number(mobile_number="+91000000")
        self.assertTrue(is_user_exists)
        self.assertEqual(user.mobile_number, "+91000000")
        self.assertEqual(user.firstname, "John")
        self.assertEqual(user.lastname, "Doe")
        self.assertFalse(user.has_usable_password())

        user, is_user_exists = get_user_by_mobile_number(mobile_number="+911111111")
        self.assertFalse(is_user_exists)

    def test_is_user_active(self):
        """Test is user active"""
        User = get_user_model()
        user = User(username="+91000000", 
                    mobile_number="+91000000", 
                    firstname="John", 
                    lastname="Doe")
        user.set_unusable_password()
        user.save()

        user, _ = get_user_by_mobile_number(mobile_number="+91000000")
        self.assertFalse(is_user_active(user))

