from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from myapp.models import Event
from myapp.views import cortex
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class CortexViewTestCase(TestCase):
    """
    Test case for Cortex views.
    """
    def setUp(self):
        """
        Set up test data including a test user, groups, and an event.
        """

        grupos = Group.objects.all()

        # Crea un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password')
        # Crea un grupo de prueba (grupo 1)
        self.group_1 = Group.objects.create(id=1)
        # Asigna el usuario al grupo 1
        self.user.groups.add(self.group_1)
        # Crea un evento de prueba
        self.event = Event.objects.create(
            titulo='Test Event',
            fecha_inicio='2024-01-01',
            fecha_fin='2024-01-02',
            estado_solicitud='En curso',
            presupuesto=1000  # Proporciona un valor para el presupuesto
        )

        #Crea un objeto de la fábrica de solicitudes para simular solicitudes HTTP
        self.factory = RequestFactory()

        # Crea un cliente de prueba
        self.client = Client()


    def test_home_view(self):
        """
        Test the home view.
        """
        # Crea un cliente de prueba
        client = Client()

        # Obtiene la respuesta de la vista utilizando el cliente de prueba
        response = client.get(reverse('home'))  # Asegúrate de que 'home' sea el nombre de la URL de la vista home

        # Verifica que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que se haya utilizado la plantilla 'home.html'
        self.assertTemplateUsed(response, 'home.html')

    def test_index_view_group_1(self):
        """
        Test the index view for users in group 1.
        """

        # Inicia sesión como el usuario en el grupo 1
        self.client.login(username='testuser', password='password')

        # Obtiene la respuesta de la vista index
        response = self.client.get(reverse('index'))  # Asegúrate de que 'index' sea el nombre de la URL de la vista index

        # Verifica que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que se haya utilizado la plantilla 'index1.html'
        self.assertTemplateUsed(response, 'index1.html')

    def test_index_view_no_group(self):
        """
        Test the index view for users with no group.
        """
        # Obtiene la respuesta de la vista utilizando el cliente de prueba
        response = self.client.get(reverse('index'))  # Asegúrate de que 'index' sea el nombre correcto de la URL de la vista index

        # Verifica que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que se haya utilizado la plantilla 'index3.html'
        self.assertTemplateUsed(response, 'index3.html')


    def test_index_view_group_2(self):
        """
        Test the index view for users in group 2.
        """
        # Prueba la vista index para un usuario en el grupo 2
        user = User.objects.create_user(username='testuser2', password='password')


        try:
            # Intenta obtener el grupo con el nombre dado
            group_2 = Group.objects.get(name='Group 2')
        except Group.DoesNotExist:
            # Si el grupo no existe, créalo
            group_2 = Group.objects.create(name='Group 2')


        user.groups.add(group_2)
        client = Client()

        client.login(username='testuser2', password='password')

        # Simular una solicitud GET a la vista index
        response = self.client.get('/')

        # Verificar el código de estado de la respuesta y la plantilla utilizada
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')




