from django.test import TestCase
from django.urls import reverse, resolve
from join_backend.views import set_csrf_token, LoginView, UserRegistrationView, UserDetailsView, ContactListCreateView, ContactDetailView, CategoryListCreateAPIView, CategoryDetailAPIView, SubtaskListCreateAPIView, SubtaskDetailAPIView, TaskListCreateAPIView, TaskDetailAPIView





class TestUrls(TestCase):
    """
TestUrls
Tests the URL routing configuration of the application, ensuring that each named URL correctly resolves to its intended view function or class.
1. test_set_csrf_url
Verifies that the set-csrf URL resolves to the set_csrf_token function.
2. test_login_url
Verifies that the login URL resolves to the LoginView class.
3. test_signup_url
Verifies that the user-register URL resolves to the UserRegistrationView class.
4. test_user_details_url
Verifies that the user-details URL resolves to the UserDetailsView class.
5. test_add_contact_url
Verifies that the add_contact URL resolves to the ContactListCreateView class.
6. test_contact_detail_url
Verifies that the contact_detail URL resolves to the ContactDetailView class, correctly passing a contact ID as an argument.
7. test_category_list_url
Verifies that the category-list URL resolves to the CategoryListCreateAPIView class.
8. test_category_detail_url
Verifies that the category-detail URL resolves to the CategoryDetailAPIView class, correctly passing a category ID as an argument.
9. test_subtask_list_url
Verifies that the subtask-list URL resolves to the SubtaskListCreateAPIView class.
10. test_subtask_detail_url
Verifies that the subtask-detail URL resolves to the SubtaskDetailAPIView class, correctly passing a subtask ID as an argument.
11. test_task_list_url
Verifies that the task-list URL resolves to the TaskListCreateAPIView class.
12. test_task_detail_url
Verifies that the task-detail URL resolves to the TaskDetailAPIView class, correctly passing a task ID as an argument.
"""
    def test_set_csrf_url(self):
        url = reverse('set-csrf')
        self.assertEqual(resolve(url).func, set_csrf_token)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_signup_url(self):
        url = reverse('user-register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    def test_user_details_url(self):
        url = reverse('user-details')
        self.assertEqual(resolve(url).func.view_class, UserDetailsView)

    def test_add_contact_url(self):
        url = reverse('add_contact')
        self.assertEqual(resolve(url).func.view_class, ContactListCreateView)

    def test_contact_detail_url(self):
        url = reverse('contact_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ContactDetailView)

    def test_category_list_url(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).func.view_class, CategoryListCreateAPIView)

    def test_category_detail_url(self):
        url = reverse('category-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, CategoryDetailAPIView)

    def test_subtask_list_url(self):
        url = reverse('subtask-list')
        self.assertEqual(resolve(url).func.view_class, SubtaskListCreateAPIView)

    def test_subtask_detail_url(self):
        url = reverse('subtask-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, SubtaskDetailAPIView)

    def test_task_list_url(self):
        url = reverse('task-list')
        self.assertEqual(resolve(url).func.view_class, TaskListCreateAPIView)

    def test_task_detail_url(self):
        url = reverse('task-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, TaskDetailAPIView)
