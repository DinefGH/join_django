import json, logging
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, LoginHistory
from .serializers import UserRegistrationSerializer, UserDetailsSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .forms import ContactForm
from django.http import JsonResponse
from django.views.decorators.http import require_safe
from rest_framework.decorators import api_view
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from .models import Subtask
from .serializers import SubtaskSerializer
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate




User = get_user_model()



@method_decorator(csrf_exempt, name='dispatch')

class LoginView(APIView):
    permission_classes = [AllowAny]
    """
LoginView:

Handles user authentication by verifying credentials (email and password) 
and returning an authentication token along with user details if successful, or an error message if not.
"""
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Authentication was successful
            token, created = Token.objects.get_or_create(user=user)
            # Serialize the user data
            user_data = UserDetailsSerializer(user).data
            LoginHistory.objects.create(
                user=user,
                token=token.key,
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            return Response({"token": token.key, "user": user_data}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    



@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for this view

    """
    UserRegistrationView:

    Manages user registration by validating the submitted data and creating a new user in the system if the data is valid, 
    returning a success message upon successful registration.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserDetailsView(APIView):
    """
UserDetailsView:

Provides details of the currently authenticated user, accessible only to authenticated users, 
by serializing the user’s data and returning it in the response.
"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class ContactCreateView(LoginRequiredMixin, CreateView):
    """
ContactCreateView:

A view for creating new contacts, accessible only to logged-in users. 
It associates the new contact with the currently authenticated user and redirects to a success page upon successful form submission.
"""
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/add_contact.html'
    success_url = reverse_lazy('contact_success')  # Adjust as necessary

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user
        return super().form_valid(form)
    

"""
set_csrf_token:

A view that sets the CSRF token for the current session, 
responding with a JSON message to indicate that the token has been set.
"""

@require_safe
def set_csrf_token(request):
    return JsonResponse({'detail': 'CSRF token set'})




class ContactListCreateView(generics.ListCreateAPIView):
    """
ContactListCreateView:

Handles the retrieval and creation of Contact objects for the currently authenticated user. 
Filters the contacts based on the user and ensures that new contacts are associated with the user making the request.
"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)

    def perform_create(self, serializer):
        print("Authorization Header:", self.request.headers.get('Authorization'))
        # Automatically set the user field to the currently authenticated user
        serializer.save(user=self.request.user)




class ContactDetailView(APIView):
    """
ContactDetailView:

Provides detailed view, update, and deletion capabilities for individual contacts based on their ID. 
Handles errors such as when a contact is not found, ensuring appropriate responses are returned.
"""
    """
    Retrieve a contact by id.
    """
    def get(self, request, id):
        try:
            contact = Contact.objects.get(pk=id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, id):
        try:
            contact = Contact.objects.get(pk=id)
            contact.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, id):
        contact = get_object_or_404(Contact, pk=id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class CategoryListCreateAPIView(APIView):
    """
CategoryListCreateAPIView:

Manages the listing of all categories and the creation of new categories. 
It handles the serialization and validation of category data for GET and POST requests.
"""
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CategoryDetailAPIView(APIView):
    """
CategoryDetailAPIView:

Handles retrieval, updating, and deletion of specific categories based on their ID. 
Ensures that appropriate responses are returned for successful operations or when a category is not found.
"""
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is not Response:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return category

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is not Response:
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return category

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is not Response:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return category
    



class SubtaskListCreateAPIView(APIView):
    """
SubtaskListCreateAPIView:

Manages the listing and creation of subtasks. 
Allows for the retrieval of all subtasks and the creation of new ones, validating and serializing the data as needed.
"""
    def get(self, request):
        subtasks = Subtask.objects.all()
        serializer = SubtaskSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SubtaskDetailAPIView(APIView):
    """
SubtaskDetailAPIView:

Handles the retrieval, updating, and deletion of specific subtasks based on their ID. 
Ensures correct handling of requests, including returning errors if the subtask is not found.
"""
    def get_object(self, pk):
        try:
            return Subtask.objects.get(pk=pk)
        except Subtask.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not isinstance(subtask, Response):
            serializer = SubtaskSerializer(subtask)
            return Response(serializer.data)
        return subtask

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not isinstance(subtask, Response):
            serializer = SubtaskSerializer(subtask, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return subtask

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not isinstance(subtask, Response):
            subtask.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return subtask
    




class TaskListCreateAPIView(APIView):
    """
TaskListCreateAPIView:

Manages the listing and creation of tasks associated with the currently authenticated user. 
Handles task creation with nested subtasks and relationships to contacts and categories.
"""
    def get(self, request):
        tasks = Task.objects.filter(creator=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Log the incoming data
        print("Received data:", request.data)  # Log the raw data

        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log the serializer errors
            print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

logger = logging.getLogger(__name__)



class TaskDetailAPIView(APIView):
    """
TaskDetailAPIView:

Provides detailed view, update, and deletion capabilities for individual tasks based on their ID. 
Handles complex updates, including managing subtasks and ensuring data integrity during task modifications.
"""
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'message': 'The task does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        task = self.get_object(pk)
        if isinstance(task, Response):
            return task
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        if isinstance(task, Response):
            return task

        serializer = TaskSerializer(task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_task = serializer.save()

            # Handle subtasks
            subtasks_data = request.data.get('subtasks', [])
            existing_subtask_ids = set(task.subtasks.values_list('id', flat=True))

            print(f"Existing subtask IDs: {existing_subtask_ids}")
            print(f"Received subtasks data: {subtasks_data}")

            incoming_subtask_ids = {subtask_data.get('id') for subtask_data in subtasks_data if subtask_data.get('id')}
            print(f"Incoming subtask IDs: {incoming_subtask_ids}")

            # Update existing subtasks
            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id')
                if subtask_id in existing_subtask_ids:
                    # Update existing subtask
                    Subtask.objects.filter(id=subtask_id).update(**subtask_data)
                    print(f"Updated subtask ID: {subtask_id}")
                elif subtask_id is None:
                    # Create new subtask and associate with the task
                    new_subtask = Subtask.objects.create(**subtask_data)
                    updated_task.subtasks.add(new_subtask)
                    print(f"Created new subtask with ID: {new_subtask.id}")
                else:
                    print(f"Subtask ID {subtask_id} not found in existing subtasks")
                    return Response({'message': f'Subtask ID {subtask_id} not found'}, status=status.HTTP_400_BAD_REQUEST)

            # Remove subtasks that are not in the request data
            for subtask_id in existing_subtask_ids - incoming_subtask_ids:
                Subtask.objects.filter(id=subtask_id).delete()
                print(f"Removed subtask ID: {subtask_id}")

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if isinstance(task, Response):
            return task
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)