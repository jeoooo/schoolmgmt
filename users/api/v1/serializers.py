from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'phone', 'college', 'department', 'employee_id', 
            'student_id', 'date_of_birth', 'address', 'is_active',
            'date_created', 'date_updated', 'password'
        ]
        read_only_fields = ['id', 'date_created', 'date_updated']

    def validate_password(self, value):
        """
        Validate password using Django's password validators
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        """
        Create a new user with encrypted password
        """
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update user instance
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name', 'role', 'phone', 'college', 
            'department', 'employee_id', 'student_id', 'date_of_birth', 'address'
        ]

    def validate(self, attrs):
        """
        Validate that password and password_confirm match
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_role(self, value):
        """
        Validate role assignment
        """
        # Only admins can create other admins
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if value == 'admin' and not request.user.is_admin():
                raise serializers.ValidationError("Only admins can create admin users")
        return value

    def create(self, validated_data):
        """
        Create user with validated data
        """
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """
        Validate login credentials
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, 
                password=password
            )
            
            if not user:
                raise serializers.ValidationError('Invalid login credentials')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (read-only for sensitive fields)
    """
    college_name = serializers.CharField(source='college.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone', 'college', 'college_name',
            'department', 'department_name', 'employee_id', 'student_id',
            'date_of_birth', 'address', 'is_active', 'date_created'
        ]
        read_only_fields = [
            'id', 'username', 'role', 'college', 'department', 
            'employee_id', 'student_id', 'is_active', 'date_created'
        ]

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()

    def validate(self, attrs):
        """
        Validate password change
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

    def validate_old_password(self, value):
        """
        Validate old password
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
