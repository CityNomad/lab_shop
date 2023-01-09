from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Profile(models.Model):
    birthday = models.DateField(null=True, blank=True, verbose_name="Birthday")
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True, verbose_name="Avatar")
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name="User",
                                related_name="profile")

    def __str__(self):
        return f"{self.id}. {self.user}: {self.birthday}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

