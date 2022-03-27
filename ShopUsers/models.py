from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    picture = models.ImageField(default='default.jpg',upload_to='users')

    def __repr__(self):
        return self.user.username
    class Meta:
        verbose_name='Профиль'
        verbose_name_plural='Профили'
