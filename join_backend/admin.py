from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from .models import CustomUser, Contact, Category, LoginHistory, Task, Subtask
from django.utils.translation import gettext_lazy as _





class ContactAdmin(admin.ModelAdmin):
    """
ContactAdmin:

Manages the display, filtering, and searching of Contact records in the admin interface. 
Allows admins to view and manage contacts based on user and other criteria.
"""
    list_display = ('name', 'email', 'phone', 'color', 'user', 'id')  # Columns to display in the admin list view
    list_filter = ('user',)  # Filters by user in the sidebar
    search_fields = ('name', 'email', 'phone')  # Fields to search by in the admin
    ordering = ('user', 'name')  # Default ordering
    raw_id_fields = ('user',)  # Use a lookup widget for user field

admin.site.register(Contact, ContactAdmin)




class CustomUserAdmin(admin.ModelAdmin):
    """
CustomUserAdmin:

Configures the admin interface for managing CustomUser records, including displaying key user details, 
managing permissions, and controlling the registration and search functionalities.
"""
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_staff']
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)





class CategoryAdmin(admin.ModelAdmin):
    """
CategoryAdmin:

Handles the display and search capabilities for Category records in the admin interface, 
with filters available for color and name.
"""
    list_display = ('name', 'color')  # Fields to be displayed in the admin list view
    search_fields = ('name',)  # Fields to search by in the admin
    list_filter = ('color', 'name',)  # Filters by color in the sidebar


admin.site.register(Category, CategoryAdmin)




class SubtaskInline(admin.TabularInline):
    """
SubtaskInline:

Defines an inline admin interface for managing Subtasks directly within the Task editing interface, 
facilitating the addition of multiple subtasks.
"""
    model = Subtask
    extra = 1




class TaskAdmin(admin.ModelAdmin):
    """
TaskAdmin:

Manages the Task records in the admin interface, providing options to filter, 
search, and order tasks by priority, due date, and other key attributes.
"""
    list_display = ('title', 'priority', 'due_date', 'category', 'creator', 'status')
    list_filter = ('priority', 'due_date', 'category', 'creator', 'status')
    search_fields = ('title', 'description', 'creator__name', 'status')

admin.site.register(Task, TaskAdmin)



class SubtaskAdmin(admin.ModelAdmin):
    """
SubtaskAdmin:

Configures the display and filtering options for Subtasks in the admin interface, 
allowing for efficient management of subtask completion status and details.
"""
    list_display = ['text', 'completed', 'id']  # Adjust fields to display as needed
    list_filter = ['completed']  # Filter options
    search_fields = ['text']  # Search functionality based on text field

admin.site.register(Subtask, SubtaskAdmin)



class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'user_agent', 'login_time')
    search_fields = ('user__username', 'user__email', 'token', 'user_agent')
    list_filter = ('login_time',)
    readonly_fields = ('user', 'token', 'user_agent', 'login_time')

admin.site.register(LoginHistory, LoginHistoryAdmin)