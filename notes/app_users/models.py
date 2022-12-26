from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.IntegerField(null=True, verbose_name=_('номер телефона'))
	date_of_birth = models.DateTimeField(null=True, verbose_name=_('дата рождения'))
