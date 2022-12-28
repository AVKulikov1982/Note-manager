from django.urls import path, include
from .views import NotesListView, NoteDetailView, UpdateNote, DeleteNote, AddNote

urlpatterns = [
	path('notes', NotesListView.as_view(), name='list_notes'),
	path('notes/<int:pk>', NoteDetailView.as_view(), name='detail_note'),
	path('notes/<param>', NotesListView.as_view(), name='list_notes_with_param'),
	path('add_note', AddNote.as_view(), name='add_note'),
	path('notes/<int:pk>/update', UpdateNote.as_view(), name='update_note'),
	path('notes/<int:pk>/delete', DeleteNote.as_view(), name='delete_note'),
]
