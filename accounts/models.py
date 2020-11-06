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


@receiver(post_save, sender=get_user_model())
def update_user_profile(sender, instance, created, **kwargs):
    """
    При сохранении аккаунта привязывает к нему новый профиль
    """
    if created:
        from profiles.models import Profile

        Profile.objects.create(user=instance)
    instance.profile.save()
