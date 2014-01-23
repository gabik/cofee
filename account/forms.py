from django import forms

class login_client_form(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput, max_length=100)
