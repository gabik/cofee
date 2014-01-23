from django.contrib import admin
from account.models import client_profile, branch_profile

admin.site.register(client_profile)
admin.site.register(branch_profile)

