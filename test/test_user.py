import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class UserTestCase(TestCase):

    def setUp(self):
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
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.user.is_staff, False)

    def test_super_user_creation(self):
        self.assertEqual(self.superUser.is_active, True)
        self.assertEqual(self.superUser.is_superuser, True)
        self.assertEqual(self.superUser.is_staff, True)

    def test_add_user_to_group(self):
        id = 1
        group = Group.objects.get(id=id)
        group.user_set.add(self.user)
        self.assertEqual(self.user.groups.values_list(
            "id", flat=True).first(), 1)
        self.assertEqual(self.user.groups.values_list(
            "name", flat=True).first(), "LiderDeProyecto")

    def change_user_of_group(self):
        id = 1
        group = Group.objects.get(id=id)
        group.user_set.add(self.user)
        self.assertEqual(self.user.groups.values_list(
            "id", flat=True).first(), 1)
        self.assertEqual(self.user.groups.values_list(
            "name", flat=True).first(), "LiderDeProyecto")
        self.user_obj.groups.clear()
        id = 3
        group = Group.objects.get(id=id)
        group.user_set.add(self.user)
        self.assertEqual(self.user.groups.values_list(
            "id", flat=True).first(), 3)
        self.assertEqual(self.user.groups.values_list(
            "name", flat=True).first(), "MiembroComunidadAcademica")
