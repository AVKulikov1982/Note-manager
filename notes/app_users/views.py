from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import generic, View
from django.utils.translation import gettext_lazy as _
from .models import Profile
from .forms import RegisterForm, UpdateProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse


class UserLoginView(LoginView):
	template_name = 'login.html'


class AjaxUserLoginView(View):
	
	def get(self, request):
		form = AuthenticationForm()
		return render(request, template_name='login.html', context={'form': form})
	
	
	def post(self, request):
		
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		if username and password:
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return JsonResponse(data={'status': 200}, status=200)
			return JsonResponse(
				data={'error': 'Пароль и логин не валидные'},
				status=400
			)
		return JsonResponse(
				data={'error': 'Введите пароль и логин'},
				status=400
			)
		
class UserLogoutView(LogoutView):
	template_name = 'logout.html'


class UpdateProfileView(View):

	@staticmethod
	def get(request, user_id):
		user = User.objects.get(id=user_id)
		user_form = UpdateProfileForm(instance=user)
		if Profile.objects.filter(user_id=user_id):
			profile_update = Profile.objects.get(user_id=user_id)
			update_form = UpdateProfileForm(instance=profile_update)
		else:
			update_form = UpdateProfileForm(instance=user)
			
		return render(request, 'profile_update.html',
					  context={'user_form': user_form, 'update_form': update_form})

	@staticmethod
	def post(request, user_id):
		user = User.objects.get(id=user_id)
		if Profile.objects.filter(user_id=user_id):
			profile_update = Profile.objects.get(user_id=user_id)
			update_form = UpdateProfileForm(request.POST, instance=profile_update)
		else:
			update_form = UpdateProfileForm(instance=user)

		if update_form.is_valid():
			user.username = update_form.cleaned_data.get('username')
			user.first_name = update_form.cleaned_data.get('first_name')
			user.last_name = update_form.cleaned_data.get('last_name')
			user.email = update_form.cleaned_data.get('email')
			user.save()
			values_for_update = {'user': user}
			Profile.objects.update_or_create(user_id=user_id, defaults=values_for_update)
			if update_form.cleaned_data.get('new_pass1') \
					and update_form.cleaned_data.get('new_pass1') == update_form.cleaned_data.get('new_pass2'):
				user.set_password(update_form.cleaned_data.get('new_pass1'))
				user.save()

		return redirect('/')


def register(request):
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user = register_form.save()
			Profile.objects.create(user=user)
			username = register_form.cleaned_data.get('username')
			row_password = register_form.cleaned_data.get('password1')

			user = authenticate(username=username, password=row_password)
			login(request, user)
			return render(request, 'index.html')
	else:
		register_form = RegisterForm()
	return render(request, 'registration.html', context={'register_form': register_form})


def profile(request, user_id):
	if request.user.is_superuser:
		Profile.objects.get_or_create(user_id=user_id)
	return render(request, 'profile.html')
