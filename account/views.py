from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from account.forms import login_client_form
from django.forms.util import ErrorList


def create_user(request):
	return render_to_response('registration/create_user.html')

def login_client(request):
	username = password = ''
	if request.POST:
		loginform = login_client_form(request.POST)
		if loginform.is_valid():
			username = loginform.cleaned_data['username']
			password = loginform.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('after-login')
				else:
					loginform._errors["username"] = ErrorList([u"User is disabled"])
			else:
				loginform._errors["username"] = ErrorList([u"Bad username or password"])
	else:
		loginform = login_client_form()

	return render(request, 'registration/login-client.html',{'loginform': loginform})


