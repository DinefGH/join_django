from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from join_backend.models import Contact
from join_backend.models import Category
from join_backend.models import Task, Subtask, Category, Contact, CustomUser

User = get_user_model()




class LoginViewTest(TestCase):
    """
LoginViewTest:

Tests the LoginView, focusing on successful login with valid credentials, 
failure with invalid credentials, and handling of missing fields in the login request.
"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )
        self.url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.url, {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

    def test_login_invalid_credentials(self):
        response = self.client.post(self.url, {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid Credentials')

    def test_login_missing_fields(self):
        response = self.client.post(self.url, {
            'email': 'testuser@example.com'
            # Missing password field
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

        response = self.client.post(self.url, {
            'password': 'testpassword'
            # Missing email field
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)




class UserRegistrationViewTest(APITestCase):
    """
UserRegistrationViewTest:

Tests the UserRegistrationView, ensuring that a new user can be successfully registered 
and that appropriate validation errors are raised for invalid or incomplete registration data.
"""
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-register')

    def test_registration_success(self):
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'newpassword',
            'confirmPassword': 'newpassword'
        }
        response = self.client.post(self.url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully')
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())




class UserDetailsViewTest(APITestCase):
    """
UserDetailsViewTest:

Tests the UserDetailsView, verifying that an authenticated user can retrieve their own details, 
and checks the response for accuracy and correct status codes.
"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('user-details')

    def test_get_user_details(self):
        response = self.client.get(self.url)
        if response.status_code != status.HTTP_200_OK:
            print("Response Data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')
        self.assertEqual(response.data['name'], 'Test User')





class ContactCreateViewTest(TestCase):
    """
ContactCreateViewTest:

Tests the ContactCreateView, ensuring that a logged-in user can successfully create a new contact 
and that the contact is correctly saved to the database.
"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@example.com', name='testuser', password='testpassword')
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_contact_create_view(self):
        url = reverse('add_contact')
        data = {
            'name': 'Test Contact',
            'email': 'testcontact@example.com',
            'phone': '1234567890',
            'color': '#FFFFFF'  # Include the color field
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Contact.objects.filter(name='Test Contact').exists())




class ContactListCreateViewTest(APITestCase):
    """
ContactListCreateViewTest:

Tests the ContactListCreateView, verifying that a user can retrieve a list of their contacts and create new contacts. 
It ensures that only the authenticated user's contacts are returned and that new contacts are properly associated with the user.
"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', name='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_contact_list(self):
        Contact.objects.create(name='Test Contact', email='testcontact@example.com', phone='1234567890', user=self.user, color='#FFFFFF')
        url = reverse('add_contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['email'], 'testuser@example.com')

    def test_contact_create(self):
        url = reverse('add_contact')
        data = {
            'name': 'New Contact',
            'email': 'newcontact@example.com',
            'phone': '0987654321',
            'color': '#FFFFFF'  # Include the color field
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Contact.objects.filter(name='New Contact').exists())




class ContactDetailViewTest(APITestCase):
    """
ContactDetailViewTest:

Tests the ContactDetailView, covering the retrieval, update, and deletion of specific contacts. 
It ensures that these operations work as expected and return the correct status codes and data.
"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', name='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.contact = Contact.objects.create(name='Test Contact', email='testcontact@example.com', phone='1234567890', user=self.user, color='#FFFFFF')

    def test_contact_retrieve(self):
        url = reverse('contact_detail', kwargs={'id': self.contact.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Contact')
        self.assertEqual(response.data['user']['email'], 'testuser@example.com')

    def test_contact_update(self):
        url = reverse('contact_detail', kwargs={'id': self.contact.id})
        data = {
            'name': 'Updated Contact',
            'email': 'updatedcontact@example.com',
            'phone': '1112223333',
            'color': '#000000'  # Include the color field
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, 'Updated Contact')

    def test_contact_delete(self):
        url = reverse('contact_detail', kwargs={'id': self.contact.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())





class CategoryListCreateAPIViewTest(APITestCase):
    """
CategoryListCreateAPIViewTest:

Tests the CategoryListCreateAPIView, focusing on the retrieval of all categories and the creation of new categories, 
ensuring that the operations return the correct responses and status codes.
"""
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('category-list')

    def test_category_list(self):
        Category.objects.create(name='Category 1', color='#FFFFFF')
        Category.objects.create(name='Category 2', color='#000000')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_category_create(self):
        data = {'name': 'New Category', 'color': '#FF5733'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Category.objects.filter(name='New Category').exists())




class CategoryDetailAPIViewTest(APITestCase):
    """
CategoryDetailAPIViewTest:

Tests the CategoryDetailAPIView, covering the retrieval, update, and deletion of specific categories by their ID. 
It ensures that these operations handle the data correctly and return appropriate status codes.
"""
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Category 1', color='#FFFFFF')
        self.url = reverse('category-detail', kwargs={'pk': self.category.pk})

    def test_category_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Category 1')

    def test_category_update(self):
        data = {'name': 'Updated Category', 'color': '#000000'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_category_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())




class SubtaskListCreateAPIViewTest(APITestCase):
    """
SubtaskListCreateAPIViewTest:

Tests the SubtaskListCreateAPIView, verifying that subtasks can be listed and created. 
It ensures that the correct status codes and data are returned for these operations.
"""
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('subtask-list')

    def test_subtask_list(self):
        Subtask.objects.create(text='Subtask 1', completed=False)
        Subtask.objects.create(text='Subtask 2', completed=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_subtask_create(self):
        data = {'text': 'New Subtask', 'completed': False}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Subtask.objects.filter(text='New Subtask').exists())




class SubtaskDetailAPIViewTest(APITestCase):
    """
SubtaskDetailAPIViewTest:

Tests the SubtaskDetailAPIView, covering the retrieval, update, and deletion of specific subtasks. 
It ensures that these operations are handled correctly and return appropriate status codes.
"""
    def setUp(self):
        self.client = APIClient()
        self.subtask = Subtask.objects.create(text='Subtask 1', completed=False)
        self.url = reverse('subtask-detail', kwargs={'pk': self.subtask.pk})

    def test_subtask_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['text'], 'Subtask 1')

    def test_subtask_update(self):
        data = {'text': 'Updated Subtask', 'completed': True}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.subtask.refresh_from_db()
        self.assertEqual(self.subtask.text, 'Updated Subtask')

    def test_subtask_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Subtask.objects.filter(pk=self.subtask.pk).exists()) 




class TaskListCreateAPIViewTest(APITestCase):
    """
TaskListCreateAPIViewTest:

Tests the TaskListCreateAPIView, focusing on the creation of tasks by an authenticated user. 
It verifies that the task is correctly saved to the database and associated with the user.
"""
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', 
            name='Test User', 
            password='testpassword'
        )
        # Authenticate the client with the created user
        self.client.force_authenticate(user=self.user)
        self.url = reverse('task-list')  # Ensure this is the correct URL name for your view

    def test_task_create(self):
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'Medium',
            'creator': self.user.id  # The creator should be automatically assigned in the view, not passed in the data
        }
        response = self.client.post(self.url, data, format='json')

        # Print the response data for debugging
        print("Response data:", response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(title='New Task').exists())





class TaskDetailAPIViewTest(APITestCase):
    """
TaskDetailAPIViewTest:

Tests the TaskDetailAPIView, covering the retrieval, update, and deletion of specific tasks by their ID. 
It ensures that these operations return the correct data and status codes, 
and that tasks are correctly updated or deleted.
"""
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', 
            name='Test User', 
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(
            title='Task 1', 
            description='Description 1', 
            creator=self.user, 
            priority='High'
        )
        self.url = reverse('task-detail', kwargs={'pk': self.task.pk})

    def test_task_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_task_update(self):
        data = {
            'title': 'Updated Task', 
            'description': 'Updated Description', 
            'priority': 'Medium'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())