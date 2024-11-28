from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact
from .models import Category
from .models import Subtask
from .models import Task



# Assuming get_user_model() returns your CustomUser model
User = get_user_model()



class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    **UserRegistrationSerializer**

    A serializer for registering new users, requiring `name`, `email`, `password`, and `confirmPassword` fields.
    It includes validation to ensure the `password` and `confirmPassword` match before creating a new user.
    """
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirmPassword')

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError({"confirmPassword": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Create and return a new user, given the validated data.
        """
        # Remove the confirmPassword field from the validated data.
        validated_data.pop('confirmPassword', None)

        # Use the create_user method to handle user creation.
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user
    
    


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    **UserDetailsSerializer**

    A serializer for displaying user details, specifically `id`, `name`, and `email`.
    All fields are read-only, making this serializer suitable for retrieving user information without modification.
    """
    class Meta:
        model = User
        fields = ('id', 'name', 'email')  # Specify the fields you want to include
        read_only_fields = ('id', 'name', 'email')



class ContactSerializer(serializers.ModelSerializer):
    """
    **ContactSerializer**

    A serializer for managing `Contact` objects, including fields like `id`, `user`, `name`, `email`, `phone`, and `color`.
    It embeds user details using the `UserDetailsSerializer` and treats the `user` field as read-only.
    """
    user = UserDetailsSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'user', 'name', 'email', 'phone', 'color')



class CategorySerializer(serializers.ModelSerializer):
    """
    **CategorySerializer**

    A serializer for handling `Category` objects, including the `id`, `name`, and `color` fields,
    facilitating the categorization of tasks.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']



class SubtaskSerializer(serializers.ModelSerializer):
    """
    **SubtaskSerializer**

    A serializer for creating and updating `Subtask` objects, which include `id`, `text`, and `completed` fields.
    The `create` and `update` methods are customized to handle these operations efficiently.
    """
    class Meta:
        model = Subtask
        fields = ['id', 'text', 'completed']

    def create(self, validated_data):
        return Subtask.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance



class TaskSerializer(serializers.ModelSerializer):
    """
    **TaskSerializer**

    A serializer for managing `Task` objects, including fields like:
    - `id`
    - `title`
    - `description`
    - `priority`
    - `due_date`
    - `category`
    - `assigned_to`
    - `creator`
    - `subtasks`
    - `status`

    It handles nested serialization for `subtasks` and relationships with `contacts` and `categories`.
    The `create` and `update` methods are customized to manage related data, such as `subtasks` and assigned contacts.
    """
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    assigned_to = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Contact.objects.all(),
        required=False
    )
    subtasks = SubtaskSerializer(many=True, required=False)
    creator = UserDetailsSerializer(read_only=True)




    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'category', 'assigned_to', 'creator', 'subtasks', 'status']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['creator'] = request.user

        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop('assigned_to', [])
        task = Task.objects.create(**validated_data)
        task.assigned_to.set(assigned_to_data)

        for subtask_data in subtasks_data:
            subtask = Subtask.objects.create(**subtask_data)
            task.subtasks.add(subtask)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_to_data = validated_data.pop('assigned_to', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.assigned_to.set(assigned_to_data)

        current_subtasks = {subtask.id: subtask for subtask in instance.subtasks.all()}
        print(f"Existing subtask IDs: {current_subtasks.keys()}")
        updated_subtasks = []
        incoming_subtask_ids = set()

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id:
                incoming_subtask_ids.add(subtask_id)
                print(f"Processing subtask ID: {subtask_id}")
            if subtask_id and subtask_id in current_subtasks:
                subtask = current_subtasks[subtask_id]
                for key, value in subtask_data.items():
                    setattr(subtask, key, value)
                subtask.save()
                updated_subtasks.append(subtask)
                print(f"Updated subtask: {subtask_id}")
            elif subtask_id:
                print(f"Subtask ID {subtask_id} not found in existing subtasks: {current_subtasks.keys()}")
                raise serializers.ValidationError(f"Subtask ID {subtask_id} not found in current subtasks")
            else:
                # Skip creating new subtask
                continue

        print(f"Received subtasks data: {subtasks_data}")
        print(f"Incoming subtask IDs: {incoming_subtask_ids}")

        instance.subtasks.add(*updated_subtasks)

        return instance