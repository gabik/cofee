from django.conf.urls import patterns, include, url

urlpatterns = patterns('orders.views',
	(r'make_order/$', 'send_to_branch'),
	(r'myBranch/$', 'my_branch'),
)
