import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserTestCase(TestCase):
    """
    Test case for user-related functionalities.
    """

    def setUp(self):
        """
        Setting up user instances for testing.
        """
        self.user = User.objects.create_user(
            username='Jhon',
            email='jhon@none.com',
            password='12345'
        )

        self.superUser = User.objects.create_superuser(
            username='Doe',
            email='Doe@none.com',
            password='12345'
        )

    def test_common_user_creation(self):
        """
        Test common user creation.
        """
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.user.is_staff, False)

    def test_super_user_creation(self):
        """
        Test superuser creation.
        """
        self.assertEqual(self.superUser.is_active, True)
        self.assertEqual(self.superUser.is_superuser, True)
        self.assertEqual(self.superUser.is_staff, True)

    def change_user_of_group(self):
        """
        Test changing user group.
        """
        # Scenario 1: Change user group to "LiderDeProyecto"
        id = 1
        group = Group.objects.get(id=id)
        group.user_set.add(self.user)
        self.assertEqual(self.user.groups.values_list(
            "id", flat=True).first(), 1)
        self.assertEqual(self.user.groups.values_list(
            "name", flat=True).first(), "LiderDeProyecto")

        # Scenario 2: Change user group to "MiembroComunidadAcademica"
        self.user.groups.clear()
        id = 3
        group = Group.objects.get(id=id)
        group.user_set.add(self.user)
        self.assertEqual(self.user.groups.values_list(
            "id", flat=True).first(), 3)
        self.assertEqual(self.user.groups.values_list(
            "name", flat=True).first(), "MiembroComunidadAcademica")
