from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from orders.forms import new_order_form
from orders.models import item_status,client_orders,item_size,item_strong,order_cart
from account.models import branch_profile
from django.forms.util import ErrorList
import json
from django.core import serializers
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/account/login-client/')
def send_to_branch(request):
	c = {}
	error_flag = None
	if request.POST:
		if 'branch' in request.POST:
			cur_branch = branch_profile.objects.filter(id=request.POST['branch'])
			if cur_branch is not None:
				cur_branch = cur_branch[0]
				c['order_id']=9
				c['branchID']=cur_branch.id
				return render(request, 'orders/sent_to_branch.html', c)
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

	return render(request, 'orders/new_order.html',c)

@login_required(login_url='/account/login-branch/')
def my_branch(request):
	c = {}
	cur_profile = branch_profile.objects.filter(user=request.user)
	if cur_profile:
		c["branchID"] = cur_profile[0].id
		return render(request, 'orders/branch_plot.html', c)
	return HttpResponse("Illegal user.. contact support...")

def map_status(order_status):
	status = {}
	status["Sent"] = "nonready"
	status["Ready"] = "ready"
	status["Branch"] = None
	status["Done"] = None
	status["Cart"] = None
	status["Dropped"] = None
	return status[str(order_status)]

@login_required(login_url='/account/login-branch/')
def all_branch_orders(request):
	c = {}
	ordersJson = {"count":0,"orders":[],"error":"1"};
	cur_profile = branch_profile.objects.filter(user=request.user)
	if cur_profile:
		myOrders = client_orders.objects.filter(branch=cur_profile).filter(Q(status__status="Sent") | Q(status__status="Ready"))
		if myOrders:
			orders_array = []
			for order in myOrders:
				cur_order_json = {}
				cur_status = map_status(str(order.status))
				if not cur_status:
					return HttpResponse(json.dumps(ordersJson), content_type="application/json")
				cur_order_json["state"] = cur_status
				cur_order_json["id"] = int(order.id)
				orders_array.append(cur_order_json)
			ordersJson = {}
			ordersJson["count"] = len(orders_array)
			ordersJson["orders"] = orders_array
			ordersJson["error"] = 0
		else:
			ordersJson = {"count":0,"orders":[],"error":"0"};
	return HttpResponse(json.dumps(ordersJson), content_type="application/json")

map_css_to_status = {'doready':'Ready', 'dononready':'NonReady', 'dodone':'Done'}

@csrf_exempt
def change_order_status(request):
	error=0
	if request.POST:
		if ("ostatus" in request.POST) and ("oid" in request.POST):
			cur_order_q = client_orders.objects.filter(id=request.POST["oid"])
			if cur_order_q:
				cur_order = cur_order_q[0]
				if request.POST["ostatus"] in map_css_to_status:
					cur_order.status = item_status.objects.get(status=map_css_to_status[request.POST["ostatus"]])
					cur_order.save()
					ojson = {'state': str(cur_order.status)}
					return HttpResponse(json.dumps(ojson), content_type="application/json")
				else:
					error=1
			else:
				error=2
		else:
			error=3
	else:
		error=4
	error="Error with updating DB status of order. error number:" + str(error)
	return HttpResponse(json.dumps({'error':error}), content_type="application/json")
