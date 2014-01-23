from django import forms
from account.models import branch_profile

class new_order_form(forms.Form):
	branch = forms.ChoiceField()
	strong = forms.ChoiceField()
	size = forms.ChoiceField()
	qty = forms.IntegerField(min_value=1, max_value=10,help_text="Max 10 cups.", initial=1, label="Quantity")
