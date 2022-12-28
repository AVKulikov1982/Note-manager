from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class NoteCategory(models.Model):
	name = models.CharField(max_length=50)
	
	def __str__(self):
		return self.name


class Note(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=100,db_index=True, verbose_name=_('заголовок'))
	descr = models.CharField(max_length=300, verbose_name=_('содержимое'))
	created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('дата/время создания'))
	category = models.ForeignKey(NoteCategory, db_index=True, default=None, null=True, on_delete=models.CASCADE, verbose_name=_('категория'))
	select = models.BooleanField(default=True, db_index=True, verbose_name=_('избранная'))
	
	def __str__(self):
		return self.title
