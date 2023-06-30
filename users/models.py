from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    is_developer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Developer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='developer')
    bio = models.TextField()
    job_title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.email}'

    
    @receiver(post_save, sender = CustomUser)
    def create_developer(sender,instance,created,**kwargs):
        if created and instance.is_developer:
            Developer.objects.create(user=instance)

    @receiver(post_save, sender = CustomUser)
    def save_developer(sender,instance,created,**kwargs):
        if instance.is_developer:
            instance.developer.save()


class Education(models.Model):
    university = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    start_year = models.DateField()
    end_year = models.DateField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='educations')

    def __str__(self):
        if not self.developer =='':
            return  f'{self.university} - {self.developer}'  
        return  f'{self.university}'


class Skill(models.Model):
    skill_name = models.CharField(max_length=38)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        if not self.developer =='':
            return  f'{self.skill_name} - {self.developer}'  
        return  f'{self.skill_name}'



class WorkExperience(models.Model):
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_year = models.DateField()
    end_year = models.DateField()
    description = models.TextField(blank=True)
    tech = models.TextField(blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='experiences')

    def tech_as_list(self):
        tech_list = ""
        if not self.tech == "":
            tech_list = self.tech.replace(", ", ",").split(',')
            tech_list = [x[0].upper() + x[1:] for x in tech_list]
        return tech_list

    def __str__(self):
        if not self.developer =='':
            return  f'{self.company} - {self.developer}'  
        return  f'{self.company}'

    
class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client')
    company_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.email}'

    
    @receiver(post_save, sender = CustomUser)
    def create_client(sender,instance,created,**kwargs):
        if created and instance.is_client:
            Client.objects.create(user=instance)

    # @receiver(post_save, sender = CustomUser)
    # def save_client(sender,instance,created,**kwargs):
    #     if instance.is_client:
    #         instance.client.save()
