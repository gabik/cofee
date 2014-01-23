from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout, password_reset_confirm, password_reset
from account import views

urlpatterns = patterns('account.views',
	(r'^login-branch/$', 'login_branch'),
	(r'^login-client/$', 'login_client'),
	(r'^logout/$', logout),
	(r'^new/$', 'create_user'),
)
