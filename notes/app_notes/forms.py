from django import forms
import datetime
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from .models import Note, NoteCategory


class AddNoteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['title', 'descr', 'category', 'select']


class UpdateNoteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['title', 'descr', 'category', 'select']


class FilterForm(forms.Form):
	created_at = forms.DateTimeField(required=False)
	title = forms.CharField(required=False)
	category = forms.ModelChoiceField(queryset=NoteCategory.objects, required=False)
	select = forms.BooleanField(required=False)