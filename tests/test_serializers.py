from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from join_backend.models import Contact, Category, Subtask, Task
from join_backend.serializers import UserRegistrationSerializer, UserDetailsSerializer, ContactSerializer, CategorySerializer
from join_backend.serializers import SubtaskSerializer, TaskSerializer
import datetime
from rest_framework.test import APIRequestFactory

User = get_user_model()




class UserRegistrationSerializerTest(TestCase):
    """
UserRegistrationSerializerTest:

Tests the UserRegistrationSerializer, ensuring valid user registration, verifying that the passwords match, 
and handling errors for missing or incorrect fields during registration.
"""
    def test_valid_registration(self):
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.name, 'John Doe')
        self.assertEqual(user.email, 'john.doe@example.com')
        self.assertTrue(user.check_password('password123'))

    def test_password_mismatch(self):
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'differentpassword'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('confirmPassword', serializer.errors)
        self.assertEqual(serializer.errors['confirmPassword'][0], 'Passwords must match.')

    def test_missing_fields(self):
        data = {
            'name': '',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'confirmPassword': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)




class UserDetailsSerializerTest(TestCase):
    """
UserDetailsSerializerTest:

Tests the UserDetailsSerializer, verifying that it correctly serializes user details, 
including name, email, and id, ensuring the data is accurately reflected in the serialized output.
"""
    def setUp(self):
        self.user = User.objects.create_user(name='John Doe', email='john.doe@example.com', password='password123')

    def test_user_details(self):
        serializer = UserDetailsSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertIn('id', data)



class ContactSerializerTest(TestCase):
    """
ContactSerializerTest:

Tests the ContactSerializer, ensuring that contacts are created with valid data and correctly serialized. 
It also verifies the relationship between the contact and the user, 
ensuring that user details are included in the serialized contact data.
"""
    def setUp(self):
        self.user = User.objects.create_user(name='John Doe', email='john.doe@example.com', password='password123')
        self.contact_data = {
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'phone': '1234567890',
            'color': '#FFFFFF'
        }

    def test_valid_contact_creation(self):
        serializer = ContactSerializer(data=self.contact_data)
        self.assertTrue(serializer.is_valid())
        contact = serializer.save(user=self.user)
        self.assertEqual(contact.name, 'Jane Doe')
        self.assertEqual(contact.email, 'jane.doe@example.com')
        self.assertEqual(contact.phone, '1234567890')
        self.assertEqual(contact.color, '#FFFFFF')
        self.assertEqual(contact.user, self.user)

    def test_contact_serialization(self):
        contact = Contact.objects.create(user=self.user, **self.contact_data)
        serializer = ContactSerializer(contact)
        data = serializer.data
        self.assertEqual(data['name'], 'Jane Doe')
        self.assertEqual(data['email'], 'jane.doe@example.com')
        self.assertEqual(data['phone'], '1234567890')
        self.assertEqual(data['color'], '#FFFFFF')
        self.assertIn('user', data)
        self.assertEqual(data['user']['id'], self.user.id)
        self.assertEqual(data['user']['name'], 'John Doe')
        self.assertEqual(data['user']['email'], 'john.doe@example.com')



class CategorySerializerTest(TestCase):
    """
CategorySerializerTest:

Tests the CategorySerializer, ensuring that categories are created with valid data and correctly serialized, 
verifying that both name and color fields are accurately reflected in the serialized output.
"""
    def setUp(self):
        self.category_data = {
            'name': 'Work',
            'color': '#FF0000'
        }

    def test_valid_category_creation(self):
        serializer = CategorySerializer(data=self.category_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, 'Work')
        self.assertEqual(category.color, '#FF0000')

    def test_category_serialization(self):
        category = Category.objects.create(**self.category_data)
        serializer = CategorySerializer(category)
        data = serializer.data
        self.assertEqual(data['name'], 'Work')
        self.assertEqual(data['color'], '#FF0000')




class SubtaskSerializerTest(TestCase):
    """
SubtaskSerializerTest:

Tests the SubtaskSerializer, ensuring that subtasks are created with valid data and correctly serialized, 
verifying the text and completed status of the subtask in both creation and serialization scenarios.
"""
    def setUp(self):
        self.subtask_data = {
            'text': 'Test subtask',
            'completed': False
        }

    def test_valid_subtask_creation(self):
        serializer = SubtaskSerializer(data=self.subtask_data)
        self.assertTrue(serializer.is_valid())
        subtask = serializer.save()
        self.assertEqual(subtask.text, 'Test subtask')
        self.assertFalse(subtask.completed)

    def test_subtask_serialization(self):
        subtask = Subtask.objects.create(**self.subtask_data)
        serializer = SubtaskSerializer(subtask)
        data = serializer.data
        self.assertEqual(data['text'], 'Test subtask')
        self.assertEqual(data['completed'], False)




class TaskSerializerTest(TestCase):
    """
TaskSerializerTest:

Tests the TaskSerializer, ensuring that tasks are created and updated with valid data, 
correctly associating categories, contacts, and subtasks. It verifies the relationships, including the creator of the task, 
and checks that all task attributes are properly handled during serialization and updates.
"""
    def setUp(self):
        self.user = User.objects.create_user(name='John Doe', email='john.doe@example.com', password='password123')
        self.category = Category.objects.create(name='Work', color='#FF0000')
        self.contact = Contact.objects.create(user=self.user, name='Jane Doe', email='jane.doe@example.com', phone='1234567890', color='#FFFFFF')
        self.subtask = Subtask.objects.create(text='Initial subtask', completed=False)
        self.task_data = {
            'title': 'Test task',
            'description': 'Test description',
            'priority': 'Low',
            'due_date': '2024-07-31',
            'category': self.category.id,
            'assigned_to': [self.contact.id],
            'subtasks': [{'text': 'Test subtask', 'completed': False}],
            'status': 'todo'
        }

    def test_valid_task_creation(self):
        # Create a request and assign the user
        factory = APIRequestFactory()
        request = factory.post('/tasks/')
        request.user = self.user  # Ensure the request is authenticated

        # Pass the request context to the serializer
        serializer = TaskSerializer(data=self.task_data, context={'request': request})
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        task = serializer.save()
        
        # Assert statements to verify task creation
        self.assertEqual(task.title, 'Test task')
        self.assertEqual(task.description, 'Test description')
        self.assertEqual(task.priority, 'Low')
        self.assertEqual(task.due_date, datetime.date(2024, 7, 31))
        self.assertEqual(task.category, self.category)
        self.assertIn(self.contact, task.assigned_to.all())
        self.assertEqual(task.subtasks.first().text, 'Test subtask')
        self.assertFalse(task.subtasks.first().completed)
        self.assertEqual(task.creator, self.user)

def test_task_update(self):
    task = Task.objects.create(
        title='Initial task',
        description='Initial description',
        priority='Low',
        due_date='2024-07-31',
        category=self.category,
        creator=self.user,
        status='todo'
    )
    task.assigned_to.add(self.contact)
    task.subtasks.add(self.subtask)
    
    update_data = {
        'title': 'Updated task',
        'description': 'Updated description',
        'priority': 'Medium',
        'due_date': '2024-08-15',
        'category': self.category.id,
        'assigned_to': [self.contact.id],
        'subtasks': [{'id': self.subtask.id, 'text': 'Updated subtask', 'completed': True}],
        'status': 'inProgress'
    }

    # Create a request and assign the user
    factory = APIRequestFactory()
    request = factory.put(f'/tasks/{task.id}/')
    request.user = self.user

    serializer = TaskSerializer(task, data=update_data, context={'request': request})
    self.assertTrue(serializer.is_valid(), msg=serializer.errors)
    updated_task = serializer.save()

    # Assert statements to verify task update
    self.assertEqual(updated_task.title, 'Updated task')
    self.assertEqual(updated_task.description, 'Updated description')
    self.assertEqual(updated_task.priority, 'Medium')
    self.assertEqual(updated_task.due_date, datetime.date(2024, 8, 15))
    self.assertEqual(updated_task.category, self.category)
    self.assertIn(self.contact, updated_task.assigned_to.all())
    
    # Fetch the subtask again to verify it was updated
    updated_subtask = updated_task.subtasks.get(id=self.subtask.id)
    self.assertEqual(updated_subtask.text, 'Updated subtask')
    self.assertTrue(updated_subtask.completed)
    self.assertEqual(updated_task.status, 'inProgress')