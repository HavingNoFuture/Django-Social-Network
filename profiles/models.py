from django.db import models
from django.contrib.auth import get_user_model


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


class Skill(models.Model):
    """
    Модель навыков пользователя
    """

    name = models.CharField("Название", max_length=100)

    def __str__(self):
        return self.name
