from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from rest_framework.reverse import reverse
from .models import Developer, Education, Skill, WorkExperience


import time

User = get_user_model()

# class UserCreateSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(
#                 {"password": "Password fields didn't match."})

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data['email']
#         )

#         user.set_password(validated_data['password'])
#         user.save()

#         return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class DeveloperSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
        extra_kwargs = {
            'password':{'write_only': True, 'required': True}
        }
    
    def create(self, validated_data):
        user = self.context["request"].user

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_developer = True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ClientSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2')
        extra_kwargs = {
            'password':{'write_only': True, 'required': True}
        }
    
    def create(self, validated_data):
        user = self.context["request"].user

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            is_client = True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LogInSerializer(TokenObtainPairSerializer): # new
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = {'email': str(user)}

        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token



class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('id', 'university', 'start_year', 'end_year')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


class DeveloperSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    experiences = WorkExperienceSerializer(many=True, read_only=True)
    api_url = serializers.HyperlinkedIdentityField(
        view_name='developer-detail',
        lookup_field='pk'
        )
    url = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Developer
        fields = ('url', 'api_url','id', 'bio', 'job_title', 'email', 'first_name', 'last_name', 'educations', 'skills', 'experiences')

    def get_url(self, obj):
        return f'/developers/{obj.id}/'

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return f'{obj.user.last_name}'

    def get_email(self, obj):
        return f'{obj.user.email}'