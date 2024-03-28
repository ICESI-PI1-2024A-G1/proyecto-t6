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
    
    def test_user_creation(self):         
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_superuser, False)
        
    