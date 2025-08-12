from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import models
import os
from django.core.validators import RegexValidator

from shinobi_verse.manager import CustomUserManager
from django.contrib.contenttypes.fields import GenericRelation

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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Shinobi(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    age = models.IntegerField()
    village = models.CharField(max_length=100)
    rank = models.CharField(max_length=50, choices=RANK_CHOICES)
    chakra_nature = models.CharField(max_length=100, blank=True)
    clan = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField()
    shinobi_picture = models.ImageField(upload_to='shinobi_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shinobis', null=True, blank=True)
    comments = GenericRelation('Comment', related_query_name='shinobi')
    likes = GenericRelation('Like', related_query_name='shinobi')
    approved = models.BooleanField(default=False)


class Clan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    village = models.CharField(max_length=100, blank=True)
    symbol = models.ImageField(upload_to="clan_symbols/", blank=True)
    founder = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    comments = GenericRelation('Comment', related_query_name='shinobi')
    likes = GenericRelation('Like', related_query_name='shinobi')
    approved = models.BooleanField(default=False)


class Jutsu(models.Model):
    name = models.CharField(max_length=100)
    chakra_type = models.CharField(max_length=50)
    jutsu_type = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comments = GenericRelation('Comment', related_query_name='shinobi')
    likes = GenericRelation('Like', related_query_name='shinobi')
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

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(
        max_length=50,
        validators=[
        RegexValidator(
                regex=r'^[A-Za-z0-9]*$',
                message='Nickname must be alphanumeric without spaces or special characters'
        ), 
        ], blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)     

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.avatar != self.avatar:
                if this.avatar:
                    if os.path.isfile(this.avatar.path):
                        os.remove(this.avatar.path)
        except Profile.DoesNotExist:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.avatar:
            if os.path.isfile(self.avatar.path):
                os.remove(self.avatar.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user.nickname}'s profile"
