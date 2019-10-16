from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Video

class VideoForm(forms.ModelForm):
	class Meta:
		model=Video
		fields=["file", "category"]

class EditVideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = '__all__'

class SignUpForm(UserCreationForm):
	channel_name = forms.CharField(max_length=100)

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

class LoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		help_texts = {
			'username' : None
		}