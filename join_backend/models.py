from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin




class CustomUserManager(BaseUserManager):
    """
CustomUserManager:

A custom manager for the CustomUser model, providing methods to create regular users and superusers with email, name, and password, 
ensuring that all necessary fields are set and validated.
"""
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email, name, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)




class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
CustomUser:

A custom user model that extends AbstractBaseUser and PermissionsMixin, using email as the unique identifier instead of a username. 
It includes fields for name, email, and user status, with CustomUserManager handling user creation.
"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    # Additional fields can be added here

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    



class Contact(models.Model):
    """
Contact:

A model representing a contact, linked to a user, with fields for name, email, phone, and a color attribute (stored as a hex code). 
Each contact is associated with a specific user and can be used for tasks.
"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    color = models.CharField(max_length=7, null=False, blank=False, default='#FF7A00')

    def __str__(self):
        return self.name
    



class Category(models.Model):
    """
Category:

A model for categorizing tasks, with unique name and color fields, where the color is represented by a hex code. 
Categories help organize tasks into distinct groups.
"""
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=7)  # Hex color codes

    def __str__(self):
        return self.name
    



class Task(models.Model):
    """
Task:

A model for tasks, including fields for title, description, priority, due date, and status. 
Tasks are linked to categories and contacts (assignees) and can have multiple subtasks. The status field tracks the task's progress.
"""
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inProgress', 'In Progress'),
        ('awaitFeedback', 'Await Feedback'),
        ('done', 'Done')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('Urgent', 'Urgent')])
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    assigned_to = models.ManyToManyField('Contact', related_name='tasks')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks', null=True)
    subtasks = models.ManyToManyField('Subtask', related_name='tasks', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')  # Add status field

    def __str__(self):
        return self.title




class Subtask(models.Model):
    """
Subtask:

A model representing a subtask, with a text description and a completed status. 
Subtasks are associated with tasks and help break down larger tasks into smaller, manageable components.
"""
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    

class LoginHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)