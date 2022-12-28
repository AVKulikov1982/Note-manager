from django.contrib import admin
from .models import Note, NoteCategory


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'descr', 'created_at', 'category', 'select']
    
    
@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
