from django.db import models
from django.contrib.auth.models import User

class client_profile(models.Model):
  user = models.ForeignKey(User, unique=True)
  phone_num = models.CharField(max_length=30, blank=True, null=True)
  hash = models.CharField(max_length=100, blank=True, null=True)

  def __unicode__(self):
    return self.user.username

class branch_profile(models.Model):
  user = models.ForeignKey(User, unique=True)
  phone_num = models.CharField(max_length=30, blank=True, null=True)
  address = models.CharField(max_length=50, blank=True, null=True)
  hash = models.CharField(max_length=100, blank=True, null=True)
  header = models.CharField(max_length=300, blank=True, null=True)

  def __unicode__(self):
    return self.user.username

