from django import forms
from account.models import branch_profile

class new_order_form(forms.Form):
	branch = forms.ChoiceField()
	strong = forms.ChoiceField()
	size = forms.ChoiceField()
	qty = forms.IntegerField()
