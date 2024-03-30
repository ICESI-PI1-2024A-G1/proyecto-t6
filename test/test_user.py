import pytest
from django.test import TestCase
from django.contrib.auth.models import User

class UserTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='Jhon',
            email='jhon@none.com',
            password= '12345'
        )  
        
        self.superUser = User.objects.create_superuser(
            username='Doe',
            email='Doe@none.com',
            password= '12345'
            
        )
    
    def test_common_user_creation(self):         
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.user.is_staff, False)
        
    def test_super_user_creation(self):         
        self.assertEqual(self.superUser.is_active, True)
        self.assertEqual(self.superUser.is_superuser, True)
        self.assertEqual(self.superUser.is_staff, True)
        
    