from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from orders.forms import new_order_form
from account.models import branch_profile
from django.forms.util import ErrorList

@login_required(login_url='/account/login-client/')
def send_to_branch(request):
	c = {}
	error_flag = None
	if request.POST:
		if 'branch' in request.POST:
			cur_branch = branch_profile.objects.filter(id=request.POST['branch'])
			if cur_branch is not None:
				cur_branch = cur_branch[0]
				return render(request, 'cofee/sent_to_branch.html', c)
			else:
				error_flag=1
		else:
			error_flag=1

	if error_flag:
		c['error']="Something got wrong with your request order... :("

	form = new_order_form()
	strong_choices = ([('1','Light'), ('2','Normal'),('3','Strong'), ])
	size_choices = ([('1','Small'), ('2','Normal'),('3','Big'), ])
	form.fields['branch'].choices = branch_profile.objects.all().values_list('id','header')
	form.fields['strong'].choices = strong_choices
	form.fields['size'].choices = size_choices

	c['form']=form

	return render(request, 'cofee/new_order.html',c)

