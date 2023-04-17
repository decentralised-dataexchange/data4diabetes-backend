from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        user = User(username="user001", 
                    mobile_number="+91000000", 
                    firstname="John", 
                    lastname="Doe")
        user.set_unusable_password()
        user.save()


    def test_user_created_with_mobile_number(self):
        """Test user has mobile number"""
        user = User.objects.get(username="user001")
        self.assertEqual(user.mobile_number, "+91000000")
    
    def test_user_created_with_firstname(self):
        """Test user has firstname"""
        user = User.objects.get(username="user001")
        self.assertEqual(user.firstname, "John")
    
    def test_user_created_with_lastname(self):
        """Test user has lastname"""
        user = User.objects.get(username="user001")
        self.assertEqual(user.lastname, "Doe")
    
    def test_user_created_with_no_password(self):
        """Test user with no password"""
        user = User.objects.get(username="user001")
        self.assertEqual(user.has_usable_password(), False)