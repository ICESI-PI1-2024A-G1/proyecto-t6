from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import redirect
from myapp.views import academicMembersLogin, ccsaLogin, signout

class AcademicMembersLoginTestCase(TestCase):
    """
    Test case for academic members login views.
    """
    def setUp(self):
        """
        Set up test data including a test user, group, and request factory.
        """

        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password')
        # Crea un grupo de prueba (grupo 3)
        self.group = Group.objects.create(id=3)
        # Asigna el usuario al grupo
        self.user.groups.add(self.group)


        # Crea un objeto de la fábrica de solicitudes para simular solicitudes HTTP
        self.factory = RequestFactory()


    def get_response(self, request):
        """
        Simulate the behavior of a middleware in Django.
        """
        # Este método simula el comportamiento de un middleware en Django
        return None

    def test_get_request(self):
        """
        Test a GET request.
        """
        # Simula una solicitud GET
        request = self.factory.get('/login/')
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')


    def add_session_to_request(self, request):
        """
        Add session to request.
        """
        middleware = SessionMiddleware(self.get_response)
        middleware.process_request(request)
        request.session.save()

    def test_post_request_valid_credentials(self):
        """
        Test a POST request with valid credentials.
        """
        # Crea un objeto de solicitud POST con credenciales válidas
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'password'})

        # Autentica al usuario manualmente (simulando el comportamiento del middleware de autenticación)
        user = authenticate(username='testuser', password='password')
        request.user = user

        # Agrega la sesión al objeto de solicitud
        self.add_session_to_request(request)

        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 302)  # Debería redirigir a la página de inicio


    def test_post_request_invalid_credentials(self):
        """
       Test a POST request with invalid credentials.
       """
        # Simula una solicitud POST con credenciales inválidas
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect username or password!')

    def test_post_request_invalid_group(self):
        """
        Test a POST request with valid credentials but in an incorrect group.
        """
        # Simula una solicitud POST con credenciales válidas pero en un grupo incorrecto
        # Quita el usuario del grupo 3 (grupo de prueba)
        self.user.groups.clear()
        request = self.factory.post('/login/', {'username': 'testuser', 'password': 'password'})
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credentials do not belong to an academic community member!')

class AuthViewsTestCase(TestCase):
    """
    Test case for authentication views.
    """
    def setUp(self):
        """
        Set up test data including test user, groups, and request factory.
        """
    # Elimina todos los grupos existentes
        Group.objects.all().delete()

        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password')
        # Crea un grupo de prueba (grupo 1)
        self.group_1 = Group.objects.create(name='Group1')
        # Asigna el usuario al grupo 1
        self.user.groups.add(self.group_1)
        # Crea un grupo de prueba (grupo 3)
        self.group_3 = Group.objects.create(name='Group3')
        # Crea un objeto de la fábrica de solicitudes para simular solicitudes HTTP
        self.factory = RequestFactory()

    def get_response(self, request):
        """
        Simulate the behavior of a middleware in Django.
        """
        # Este método simula el comportamiento de un middleware en Django
        return None

    def add_session_to_request(self, request):
        """
        Add session to request.
        """
        middleware = SessionMiddleware(self.get_response)
        middleware.process_request(request)
        request.session.save()

    def test_academic_members_login_get_request(self):
        """
        Test GET request for academicMembersLogin.
        """
        # Prueba la solicitud GET para academicMembersLogin
        request = self.factory.get('/academic/login/')
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_academic_members_login_post_request_valid_credentials(self):
        """
        Test POST request with valid credentials for academicMembersLogin.
        """
        # Prueba la solicitud POST con credenciales válidas para academicMembersLogin
        request = self.factory.post('/academic/login/', {'username': 'testuser', 'password': 'password'})
        user = authenticate(username='testuser', password='password')
        request.user = user
        self.add_session_to_request(request)
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)  # Debería redirigir a la página de inicio

    def test_academic_members_login_post_request_invalid_credentials(self):
        """
        Test POST request with invalid credentials for academicMembersLogin.
        """
        # Prueba la solicitud POST con credenciales inválidas para academicMembersLogin
        request = self.factory.post('/academic/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect username or password!')

    def test_academic_members_login_post_request_invalid_group(self):
        """
        Test POST request with valid credentials but user in an incorrect group for academicMembersLogin.
        """
        # Prueba la solicitud POST con credenciales válidas pero usuario en un grupo incorrecto para academicMembersLogin
        request = self.factory.post('/academic/login/', {'username': 'testuser', 'password': 'password'})
        user = authenticate(username='testuser', password='password')
        request.user = user
        self.add_session_to_request(request)
        response = academicMembersLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Credentials do not belong to an academic community member!')

    def test_ccsa_login_get_request(self):
        """
       Test GET request for ccsaLogin.
       """
        # Prueba la solicitud GET para ccsaLogin
        request = self.factory.get('/ccsa/login/')
        response = ccsaLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_ccsa_login_post_request_valid_credentials(self):
        """
        Test POST request with valid credentials for ccsaLogin.
        """
        # Prueba la solicitud POST con credenciales válidas para ccsaLogin
        request = self.factory.post('/ccsa/login/', {'username': 'testuser', 'password': 'password'})
        user = authenticate(username='testuser', password='password')
        request.user = user
        self.add_session_to_request(request)
        response = ccsaLogin(request)
        self.assertEqual(response.status_code, 302)  # Debería redirigir a la página de inicio

    def test_ccsa_login_post_request_invalid_credentials(self):
        """
        Test POST request with invalid credentials for ccsaLogin.
        """
        # Prueba la solicitud POST con credenciales inválidas para ccsaLogin
        request = self.factory.post('/ccsa/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        response = ccsaLogin(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect username or password!')

    def test_ccsa_login_post_request_invalid_group(self):
        """
        Test POST request with valid credentials but user in an incorrect group for ccsaLogin.
        """
        # Prueba la solicitud POST con credenciales válidas pero usuario en un grupo incorrecto para ccsaLogin
        request = self.factory.post('/ccsa/login/', {'username': 'testuser', 'password': 'password'})
        user = authenticate(username='testuser', password='password')
        request.user = user
        self.add_session_to_request(request)
        response = ccsaLogin(request)
        self.assertEqual(response.status_code, 302)


    def test_signout(self):
        """
        Test the signout view.
        """
        # Crea una solicitud GET para la vista de cierre de sesión
        request = self.factory.get('/signout/')

        # Agrega el middleware de sesión a la solicitud
        self.add_session_to_request(request)

        # Llama a la vista de cierre de sesión
        response = signout(request)

        # Verifica que la respuesta sea una redirección a la página de inicio
        self.assertEqual(response.status_code, 302)
