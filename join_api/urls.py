from django.contrib import admin
from django.urls import path
from join_api import settings
from join_backend.views import set_csrf_token
from join_backend.views import LoginView
from join_backend.views import UserRegistrationView, UserDetailsView, ContactListCreateView, ContactDetailView, CategoryListCreateAPIView, CategoryDetailAPIView, SubtaskListCreateAPIView, SubtaskDetailAPIView, TaskListCreateAPIView, TaskDetailAPIView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls


"""
'set-csrf/' - Sets the CSRF token.
"""
"""
'admin/' - Django admin interface.
"""
"""
'login/' - User login endpoint.
"""
"""
'signup/' - User registration endpoint.
"""
"""
'user/details/' - Retrieves user details.
"""
"""
'addcontact/' - Adds a new contact.
"""
"""
'contact/<int:id>/' - Retrieves or modifies contact details.
"""
"""
'categories/' - Lists or creates categories.
"""
"""
'categories/<int:pk>/' - Retrieves or modifies a specific category.
"""
"""
'subtasks/' - Lists or creates subtasks.
"""
"""
'subtasks/<int:pk>/' - Retrieves or modifies a specific subtask.
"""
"""
'tasks/' - Lists or creates tasks.
"""
"""
'tasks/<int:pk>/' - Retrieves or modifies a specific task.
"""

urlpatterns = [
    
    path('set-csrf/', set_csrf_token, name='set-csrf'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', UserRegistrationView.as_view(), name='user-register'),
    path('user/details/', UserDetailsView.as_view(), name='user-details'),
    path('addcontact/',ContactListCreateView.as_view(), name='add_contact'),
    path('contact/<int:id>/', ContactDetailView.as_view(), name='contact_detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('subtasks/', SubtaskListCreateAPIView.as_view(), name='subtask-list'),
    path('subtasks/<int:pk>/', SubtaskDetailAPIView.as_view(), name='subtask-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
]+ staticfiles_urlpatterns()
urlpatterns +=  debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
