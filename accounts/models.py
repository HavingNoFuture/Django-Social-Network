from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from accounts.managers import AccountManager


class User(AbstractUser):
    """
    Аккаунт пользователя.
    Основания модель пользователя
    """

    email = models.EmailField(_("email address"), unique=True)
    middle_name = models.CharField(max_length=50)
    first_login = models.DateTimeField(blank=True, null=True)

    objects = AccountManager()

    class Meta:
        verbose_name = "Аккаунт пользователя"
        verbose_name_plural = "Аккаунты пользователей"
        ordering = ("-id",)

    def __str__(self):
        return self.username


class Profile(models.Model):
    """
    Профиль пользователя
    """

    GENDER = (("male", "male"), ("female", "female"))

    user = models.OneToOneField(get_user_model(), verbose_name="Аккаунт", on_delete=models.CASCADE)
    date_of_birth = models.DateField("Дата рождения", blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to="users/%Y/%m/%d/", blank=True)
    github = models.CharField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=14)
    skills = models.ManyToManyField("Skill", related_name="users")
    gender = models.CharField(max_length=6, choices=GENDER, default="male")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        ordering = ("-id",)

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"


@receiver(post_save, sender=get_user_model())
def update_user_profile(sender, instance, created, **kwargs):
    """
    При сохранении аккаунта привязывает к нему новый профиль
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Skill(models.Model):
    """
    Модель навыков пользователя
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
