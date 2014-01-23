from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
        (r'^orders/', include('orders.urls')),
        (r'^account/', include('account.urls')),
        url(r'^admin/', include(admin.site.urls)),
)

