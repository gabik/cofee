from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from orders.forms import new_order_form, new_item_form
from orders.models import item_status,client_orders,item_size,item_strong,order_cart
from account.models import branch_profile
from django.forms.util import ErrorList
import json
from django.core import serializers
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from orders.data_sets import *

Sent_Status = "Sent"

def get_cart_info(cur_user):
	return_dict = {}
	return_dict['error']=100
	if cur_user.is_authenticated():
		cart_status_arr = item_status.objects.filter(status="Cart")
		if cart_status_arr:
			cart_status = cart_status_arr[0]
			user_order = client_orders.objects.filter(status=cart_status).filter(user=cur_user)
			if user_order:
				return_dict['error']=False
				return_dict['cart_full']=True
				items = 0
				user_orders = order_cart.objects.filter(order=user_order[0])
				for order in user_orders:
					items+=order.qty
				return_dict['itemNum']=items
				return_dict['orderNum']=user_order[0].order_num
				return_dict['order_elem']=user_order[0]
				return_dict['orders']=user_orders
			else:
				return_dict['error']=False
				return_dict['cart_full']=False
				return_dict['orders']=None
			return_dict['status'] = cart_status_arr[0]
		else:
			return_dict['error']=2
	else:
		return_dict['error']=3
	return return_dict

@login_required(login_url='/account/login-client/')
def new_order(request):
	c = {}
	error_flag = None
	cart_ok=False
	cart = get_cart_info(request.user)
	if cart:
		if cart['cart_full']:
			if cart['itemNum'] > 0:
				return HttpResponseRedirect	('./order_items')
			else:
				cart['order_elem'].delete()

		if request.POST:
			form = new_order_form(request.POST)
			form.fields['branch'].choices = branch_profile.objects.all().values_list('id','header')
			if form.is_valid():
				cur_branch = branch_profile.objects.filter(id=request.POST['branch'])
				if cur_branch is not None:
					cur_branch = cur_branch[0]
					new_order = client_orders(user=request.user, status=cart['status'], branch=cur_branch, order_num=0)
					new_order.save()
					return HttpResponseRedirect	('./order_items')
					#return render(request, 'orders/add_items.html',c)
				else:
					error_flag="Selected Branch not exist.."
			else:
				error_flag="Invalid Form: " + str(form.errors)
	else:
		error_flag = "No cart object (new_order view)"
	form = new_order_form()
	form.fields['branch'].choices = branch_profile.objects.all().values_list('id','header')
	c['form']=form
	if error_flag:
		c['error']="Something got wrong with your request order... :(" + str(error_flag)

	return render(request, 'orders/new_order.html',c)


@login_required(login_url='/account/login-client/')
def select_items(request):
	c = {}
	error_flag = None

	cart_ok=False
	cart = get_cart_info(request.user)
	if cart:
		if 'error' in cart:
			if cart['error']:
				error_flag=" Cart Error:" + cart['error']
			else:
				cart_ok=True
	else:
		error_flag=" No Cart?!"

	if cart_ok:
		if cart['cart_full']:
			if request.POST:
				form = new_item_form(request.POST)
				form.fields['strong'].choices = item_strong.objects.all().values_list('id','strong')
				form.fields['size'].choices = item_size.objects.all().values_list('id','size')
				if form.is_valid():
					cur_strong = item_strong.objects.get(id=form.cleaned_data['strong'])
					cur_size = item_size.objects.get(id=form.cleaned_data['size'])
					new_cart_item=order_cart(order=cart['order_elem'], qty=form.cleaned_data['qty'], strong=cur_strong, size=cur_size)
					new_cart_item.save()
					c['added']=True
					#error_flag="Selected Branch not exist.."
				else:
					error_flag="Invalid Form: " + str(form.errors)
		else:
			return HttpResponseRedirect	('./make_order')

	form = new_item_form()
	form.fields['strong'].choices = item_strong.objects.all().values_list('id','strong')
	form.fields['size'].choices = item_size.objects.all().values_list('id','size')
	c['form']=form

	cart = get_cart_info(request.user)
	if cart:
		if 'error' in cart:
			if cart['error']:
				error_flag=" Cart #2 Error:" + cart['error']
			else:
				items = 0
				if cart['cart_full']:
					items = cart['itemNum']
				if items > 0:
					c["itemsNum"]=items
				c['branch_header'] = cart['order_elem'].branch.header
	else:
		error_flag=" No #2 Cart?!"

	if error_flag:
		c['error']="Something got wrong with your request order... :(" + str(error_flag)

	return render(request, 'orders/add_items.html',c)


@login_required(login_url='/account/login-branch/')
def checkout_cart(request):
	c = {}
	cart = get_cart_info(request.user)
	if cart:
		if 'error' in cart:
			if cart['error']:
				error_flag=" Cart Error:" + cart['error']
			else:
				items = 0
				if cart['cart_full']:
					items = cart['itemNum']
				if items > 0:
					if 'order_elem' in cart:
						cur_order = cart['order_elem']
						sent_arr = item_status.objects.filter(status=Sent_Status)
						if sent_arr:
							cur_order.status = sent_arr[0]
							cur_order.save()
							c["itemsNum"]=items
							c['order_elem'] = cur_order
							return render(request, 'orders/sent_to_branch.html',c)
						else:
							error_flag="No Sent status at DB"
					else:
						error_flag=" cart has no order element"
				else:
					error_flag=" No items "
		else:
			error_flag=" missing error field in Cart?!"
	else:
		error_flag=" No Cart?!"

	if error_flag:
		c['error']="Something got wrong with your order checkout process... :(" + str(error_flag)

	return HttpResponseRedirect ('../make_order')


@login_required(login_url='/account/login-branch/')
def my_branch(request):
	c = {}
	cur_profile = branch_profile.objects.filter(user=request.user)
	if cur_profile:
		c["branchID"] = cur_profile[0].id
		return render(request, 'orders/branch_plot.html', c)
	return HttpResponse("Illegal user.. contact support...")


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

@login_required(login_url='/account/login-client/')
def get_user_cart(request, html=False):
	error_flag=None
	ordersJson = {'count':0}
	cart = get_cart_info(request.user)
	if cart:
		if 'error' in cart:
			if cart['error']:
				error_flag=" Cart Error:" + cart['error']
			else:
				if cart['cart_full']:
					if 'orders' in cart:
						user_orders=cart['orders']
						orders_array = []
						for order in user_orders:
							cur_order_json = {}
							cur_order_json["qty"] = order.qty
							cur_order_json["strong"] = order.strong.strong
							cur_order_json["size"] = order.size.size
							orders_array.append(cur_order_json)
						ordersJson = {}
						ordersJson["count"] = len(orders_array)
						ordersJson["orders"] = orders_array
						ordersJson["error"] = 0
					else:
						error_flag=" Cart full but no Orders"
	else:
		error_flag=" No Cart?!"

	if html:
		c={}
		if not error_flag:
			c['orders']=cart['orders']
		return render(request, 'orders/client_cart.html',c)
	else:
		if error_flag:
			error="Error getting your cart. Err#:" + str(error_flag)
			return HttpResponse(json.dumps({'error':error}), content_type="application/json")
		else:
			return HttpResponse(json.dumps(ordersJson), content_type="application/json")


@login_required(login_url='/account/login-client/')
def get_user_cart_html(request):
	error=is_cart_full(request.user)
	c={}
	if error == 1:
		cart_status = item_status.objects.filter(status="Cart")[0]
		user_order_cart = client_orders.objects.filter(status=cart_status).filter(user=request.user)[0]
		user_orders = order_cart.objects.filter(order=user_order_cart)
		c['orders']=user_orders
	return render(request, 'orders/client_cart.html',c)
