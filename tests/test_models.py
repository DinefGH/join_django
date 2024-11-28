from django.test import TestCase
from join_backend.models import CustomUser
from join_backend.models import Contact
from join_backend.models import Category
from join_backend.models import Task
from join_backend.models import Subtask
from datetime import date



class CustomUserModelTest(TestCase):
    """
CustomUserModelTest:

Tests the CustomUser model, focusing on the creation of regular users and superusers, 
verifying their attributes such as email, password, and permissions, and ensuring the correct string representation.
"""
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            password="testpassword"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email="superuser@example.com",
            name="Super User",
            password="superpassword"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertEqual(str(superuser), "superuser@example.com")




class CustomUserManagerTest(TestCase):
    """
CustomUserManagerTest:

Tests the CustomUserManager, specifically the methods for creating users and superusers. 
It verifies that users are created with the correct attributes 
and checks that appropriate exceptions are raised when required fields are missing or invalid.
"""
    def setUp(self):
        self.user_manager = CustomUser.objects

    def test_create_user(self):
        user = self.user_manager.create_user(
            email="user@example.com",
            name="Test User",
            password="password123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.name, "Test User")
        self.assertTrue(user.check_password("password123"))

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError) as cm:
            self.user_manager.create_user(
                email=None,  # Ensuring the email is None to trigger the ValueError
                name="Test User",
                password="password123"
            )
        self.assertEqual(str(cm.exception), 'The Email field must be set')

    def test_create_superuser(self):
        superuser = self.user_manager.create_superuser(
            email="superuser@example.com",
            name="Super User",
            password="superpassword"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("superpassword"))

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError) as cm:
            self.user_manager.create_superuser(
                email="superuser@example.com",
                name="Super User",
                password="superpassword",
                is_staff=False
            )
        self.assertEqual(str(cm.exception), 'Superuser must have is_staff=True.')

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError) as cm:
            self.user_manager.create_superuser(
                email="superuser@example.com",
                name="Super User",
                password="superpassword",
                is_superuser=False
            )
        self.assertEqual(str(cm.exception), 'Superuser must have is_superuser=True.')




class CustomUserManagerTest(TestCase):
    """
CustomUserManagerTest:

Tests the CustomUserManager, specifically the methods for creating users and superusers. 
It verifies that users are created with the correct attributes 
and checks that appropriate exceptions are raised when required fields are missing or invalid.
"""
    def setUp(self):
        self.user_manager = CustomUser.objects

    def test_create_superuser(self):
        superuser = self.user_manager.create_superuser(
            email="superuser@example.com",
            name="Super User",
            password="superpassword"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password("superpassword"))

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_superuser(
                email="superuser@example.com",
                name="Super User",
                password="superpassword",
                is_staff=False
            )

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            self.user_manager.create_superuser(
                email="superuser@example.com",
                name="Super User",
                password="superpassword",
                is_superuser=False
            )




class ContactModelTest(TestCase):
    """
ontactModelTest:

Tests the Contact model, ensuring that contacts are correctly created with the associated user, 
and verifying their attributes such as name, email, phone, and color.
It also checks the correct string representation of a contact.
"""
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            password="testpassword"
        )
        self.contact = Contact.objects.create(
            user=self.user,
            name="Test Contact",
            email="contact@example.com",
            phone="1234567890",
            color="#FF7A00"
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.name, "Test Contact")
        self.assertEqual(self.contact.email, "contact@example.com")
        self.assertEqual(self.contact.phone, "1234567890")
        self.assertEqual(self.contact.color, "#FF7A00")
        self.assertEqual(str(self.contact), "Test Contact")




class CategoryModelTest(TestCase):
    """
CategoryModelTest:

Tests the Category model, verifying that categories are correctly created with the specified name and color, 
and checks the string representation of a category.
"""
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            color="#123456"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.color, "#123456")
        self.assertEqual(str(self.category), "Test Category")




class TaskModelTest(TestCase):
    """
TaskModelTest:

Tests the Task model, ensuring that tasks are correctly created with all associated attributes such as title, description, 
priority, due date, category, and creator. 
It also verifies the relationships with contacts and ensures the correct string representation of a task.
"""
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            name="Test User",
            password="testpassword"
        )
        self.contact = Contact.objects.create(
            user=self.user,
            name="Test Contact",
            email="contact@example.com",
            phone="1234567890",
            color="#FF7A00"
        )
        self.category = Category.objects.create(
            name="Test Category",
            color="#123456"
        )
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            priority="Medium",
            due_date=date(2023, 12, 31),
            category=self.category,
            creator=self.user,
            status="todo"
        )
        self.task.assigned_to.add(self.contact)

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task")
        self.assertEqual(self.task.priority, "Medium")
        self.assertEqual(self.task.due_date.strftime('%Y-%m-%d'), "2023-12-31")
        self.assertEqual(self.task.category, self.category)
        self.assertEqual(self.task.creator, self.user)
        self.assertEqual(self.task.status, "todo")
        self.assertIn(self.contact, self.task.assigned_to.all())
        self.assertEqual(str(self.task), "Test Task")




class SubtaskModelTest(TestCase):
    """
SubtaskModelTest:

Tests the Subtask model, verifying that subtasks are correctly created with the specified text and completion status. 
It also checks the string representation of a subtask.
"""
    def setUp(self):
        self.subtask = Subtask.objects.create(
            text="Test Subtask",
            completed=False
        )

    def test_subtask_creation(self):
        self.assertEqual(self.subtask.text, "Test Subtask")
        self.assertFalse(self.subtask.completed)
        self.assertEqual(str(self.subtask), "Test Subtask")