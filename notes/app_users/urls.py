from django.urls import path, include
from .views import AjaxUserLoginView, UserLoginView, UserLogoutView, UpdateProfileView, register, profile

urlpatterns = [
	# path('login', UserLoginView.as_view(), name='login'),
	path('login', AjaxUserLoginView.as_view(), name='ajaxlogin'),
	path('logout', UserLogoutView.as_view(), name='logout'),
	path('registration', register, name='registration'),
	path('profile/<int:user_id>', profile, name='profile'),
	path('profile/update/<int:user_id>', UpdateProfileView.as_view(), name='profile_update'),
]