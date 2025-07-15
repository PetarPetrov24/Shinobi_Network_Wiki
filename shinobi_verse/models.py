from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import models

from shinobi_verse.manager import CustomUserManager

# Create your models here.

RANK_CHOICES = [
    ('Academy Student', 'Academy Student'), # Beginner training at ninja academy
    ('Genin', 'Genin'),  # Entry-level ninja
    ('Chunin', 'Chunin'), # Mid-level ninja with leadership potential
    ('Special Jonin', 'Special Jonin'), # Elite ninja with expertise in specific areas
    ('Jonin', 'Jonin'), # High-level ninja, often team leaders
    ('Anbu', 'Anbu'), # Elite black ops under direct Hokage control
    ('Sannin', 'Sannin'), # Legendary ninja with immense power
    ('Kage', 'Kage'),  # Village leader
    ('Rogue Ninja', 'Rogue Ninja'), # Ninja who abandoned their village
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Shinobi(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    age = models.IntegerField()
    village = models.CharField(max_length=100)
    rank = models.CharField(max_length=50, choices=RANK_CHOICES)
    chakra_nature = models.CharField(max_length=100, blank=True)
    clan = models.ForeignKey("Clan", on_delete=models.SET_NULL, null=True)
    bio = models.TextField()
    shinobi_picture = models.ImageField(upload_to='shinobi_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Clan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    village = models.CharField(max_length=100, blank=True)
    symbol = models.ImageField(upload_to="clan_symbols/", blank=True)
    founder = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    approved = models.BooleanField(default=False)


class Jutsu(models.Model):
    name = models.CharField(max_length=100)
    chakra_type = models.CharField(max_length=50)
    jutsu_type = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    liked_at = models.DateTimeField(auto_now_add=True)

