from django.urls import path

from user.api.views import (
		api_registration_view,
		APILoginView
	)

app_name = 'user'

urlpatterns = [
	path('register', api_registration_view, name='register'),
	path('login', APILoginView.as_view(), name='login')
]