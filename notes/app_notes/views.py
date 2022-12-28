from django.shortcuts import render
from django.views import generic
from .models import Note, NoteCategory
from .forms import UpdateNoteForm, AddNoteForm, FilterForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import View


class NotesListView(generic.ListView):
	
	model = Note
	template_name = 'notes_list.html'
	context_object_name = 'notes'
	
	def get_queryset(self):
		notes = Note.objects.filter(user_id=self.request.user.id)
		if self.kwargs.get('param') == 'sort_by_date':
			return notes.order_by('-created_at')
		elif self.kwargs.get('param') == 'sort_by_category':
			return notes.order_by('category__name')
		elif self.kwargs.get('param') == 'sort_by_select':
			return notes.order_by('-select')
		return Note.objects.filter(user_id=self.request.user.id)

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(NotesListView, self).get_context_data()
		context['notes'] = self.get_queryset()
		return context
	
	def post(self, request, **kwargs):
		if self.kwargs.get('param') == 'filter':
			notes = Note.objects.filter(user_id=self.request.user.id)
			filter_form = FilterForm(self.request.POST)
			print(filter_form.errors)
			try:
				if filter_form.is_valid():
					created_at = filter_form.cleaned_data.get('created_at')
					print(created_at)
					if created_at: notes=notes.filter(created_at=created_at)
					title = filter_form.cleaned_data.get('title')
					if title: notes = notes.filter(title=title)
					try:
						category = NoteCategory.objects.get(name=filter_form.cleaned_data.get('category'))
					except:
						category = None
					if category: notes = notes.filter(category=category)
					select = filter_form.cleaned_data.get('select')
					if select: notes = notes.filter(select=select)
					return render(request, template_name = 'notes_list.html', context={'notes': notes})
			except:
				return render(request, template_name = 'notes_list.html', context={'notes': notes})
		return render(request, template_name = 'notes_list.html', context={'notes': notes})

class NoteDetailView(generic.DetailView):
	model = Note
	template_name = 'note_detail.html'


class AddNote(View):

	@staticmethod
	def get(request):
		note_form = AddNoteForm()
		return render(request, 'add_note.html', context={'note_form': note_form})

	@staticmethod
	def post(request):
		note_form = AddNoteForm(request.POST)
		if note_form.is_valid():
			user = User.objects.get(username=request.user)
			title = note_form.cleaned_data.get('title')
			descr = note_form.cleaned_data.get('descr')
			category = note_form.cleaned_data.get('category')
			select = note_form.cleaned_data.get('select')
			Note.objects.create(user=user, title=title, descr=descr, category=category, select=select)
		else:
			return HttpResponseBadRequest('что-то неправильно ввели')

		return redirect('/')


class UpdateNote(View):

	@staticmethod
	def get(request, pk):
		note = Note.objects.get(id=pk)
		note_form = UpdateNoteForm(instance=note)
		return render(request, 'update_note.html', context={'note_form': note_form, 'pk': pk})

	@staticmethod
	def post(request, pk):
		note = Note.objects.get(id=pk)
		note_form = UpdateNoteForm(request.POST)

		if note_form.is_valid():
			note.title = note_form.cleaned_data.get('title')
			note.descr = note_form.cleaned_data.get('descr')
			note.category = note_form.cleaned_data.get('category')
			note.select = note_form.cleaned_data.get('select')
			note.save()
		else:
			return HttpResponseBadRequest('что-то неправильно ввели')

		return redirect('/')


class DeleteNote(View):

	@staticmethod
	def get(request, pk):
		note = Note.objects.get(id=pk)
		note.delete()
		return redirect('/')