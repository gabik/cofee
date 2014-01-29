from django.conf.urls import patterns, include, url

urlpatterns = patterns('orders.views',
	(r'make_order/$', 'send_to_branch'),
	(r'myBranch/$', 'my_branch'),
	(r'all_branch_orders/$', 'all_branch_orders'),
	(r'change_order_safe/$', 'change_order_status'),
)
