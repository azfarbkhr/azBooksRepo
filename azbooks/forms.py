from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class organizationForm(forms.ModelForm):
    class Meta:
        model = organization
        fields = '__all__'
        exclude = ['access_users']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }



class accountForm(forms.ModelForm):
    class Meta:
        model = account
        fields = '__all__'

        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_type': forms.Select(attrs={'class': 'form-control'}),
            'is_bank_account': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_sale_tax_account': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'organization': forms.HiddenInput(),
        }

        labels = {
            'code': 'Code',
            'name': 'Name',
            'account_type': 'Account Type',
            'is_bank_account': 'Is Bank Account',
            'is_sale_tax_account': 'Is Sale Tax Account',
            'organization': 'Organization',
        }

class partyForm(forms.ModelForm):
    class Meta:
        model = party
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_customer': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_supplier': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_employee': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_bank': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'organization': forms.HiddenInput(),
        }

        labels = {
            'name': 'Name',
            'legal_company_name': 'Legal Company Name',
            'is_customer': 'Is Customer',
            'is_supplier': 'Is Supplier',
            'is_employee': 'Is Employee',
            'is_bank': 'Is Bank',
            'organization': 'Organization',
        }

