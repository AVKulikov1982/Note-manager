from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View


class MainView(View):
	"""Представление главной страницы"""
	@staticmethod
	def get(request):

		return render(request, template_name='index.html')
