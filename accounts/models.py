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
    middle_name = models.CharField("Отчество", max_length=50, blank=True, null=True)
    first_login = models.DateTimeField(_("first login"), blank=True, null=True)

    objects = AccountManager()

    class Meta:
        verbose_name = "Аккаунт пользователя"
        verbose_name_plural = "Аккаунты пользователей"
        ordering = ("-id",)

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.middle_name:
            full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            full_name = f"{self.first_name} {self.last_name}"
        return full_name


class Profile(models.Model):
    """
    Профиль пользователя
    """

    GENDER = (("male", "Мужчина"), ("female", "Женщина"))

    user = models.OneToOneField(get_user_model(), verbose_name="Аккаунт", on_delete=models.CASCADE)
    date_of_birth = models.DateField("Дата рождения", blank=True, null=True)
    avatar = models.ImageField("Аватар", upload_to="users/%Y/%m/%d/", blank=True, null=True)
    github_url = models.CharField("Ссылка на Github", max_length=500, blank=True, null=True)
    bio = models.TextField("О себе", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=14, blank=True, null=True)
    skills = models.ManyToManyField("Skill", related_name="users", verbose_name="Навыки", blank=True, null=True)
    gender = models.CharField("Пол", max_length=6, choices=GENDER, blank=True, null=True)

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

    name = models.CharField("Название", max_length=100)

    def __str__(self):
        return self.name
