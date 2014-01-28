from django.db import models
from account.models import branch_profile
from django.contrib.auth.models import User


class item_status(models.Model):
  status=models.CharField(max_length=50, blank=False)

  def __unicode__(self):
    return self.status


class client_orders(models.Model):
  user = models.ForeignKey(User, unique=False)
  status = models.ForeignKey(item_status, unique=False)
  branch = models.ForeignKey(branch_profile, unique=False)

  def __unicode__(self):
    return self.user.username + ": " + str(self.id) + "> " + str(self.status)


class item_size(models.Model):
  size=models.CharField(max_length=50, blank=False)

  def __unicode__(self):
    return self.size


class item_strong(models.Model):
  strong=models.CharField(max_length=50, blank=False)

  def __unicode__(self):
    return self.strong


class order_cart(models.Model):
  order_num = models.ForeignKey(client_orders, unique=False)
  qty = models.IntegerField()
  strong = models.ForeignKey(item_strong, unique=False)
  size = models.ForeignKey(item_size, unique=False)
  
  def __unicode__(self):
    return self.order_num.id + ": " + self.qty + "-" + self.strong + "-" + self.size

