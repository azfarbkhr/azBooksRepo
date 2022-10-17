from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import json

from django.http import JsonResponse

from .models import *
from .forms import *
from .utils import *


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect("organization_create_url")
        else:
            error = "Unsuccessful registration. Invalid information."
            context = {'register_form': form, 'error': error}
            return render(request, 'registration/registration.html', context)
    else:
        form = NewUserForm()
        return render (request=request, template_name="registration/registration.html", context={"register_form":form})

@login_required
def organization_list(request):
    orgs = user_organization_access.objects.filter(user=request.user).values_list('organization_id', flat=True)
    orgs = organization.objects.filter(id__in=orgs)

    if len(orgs) == 0:
        return redirect("organization_create_url")

    return render(request, 'azbooks/organization_list.html', {'orgs': orgs})

@login_required
def organization_edit(request, org_id):
    if request.method == "POST":
        if org_id == 0:
            form = organizationForm(request.POST)
        else:
            org = organization.objects.get(pk=org_id)
            form = organizationForm(request.POST, instance=org)
        
        if form.is_valid():
            org = form.save(commit=False)
            org.save()
            if org_id == 0:
                user_organization_access.objects.create(user=request.user, organization=org)
            return redirect('organization_list_url')
    
    else:
        if org_id == 0:
            form = organizationForm()
        else:
            org = organization.objects.get(pk=org_id)
            form = organizationForm(instance=org)
    
    check_org_access(request, -1)
    
    return render(request, 'azbooks/organization_form.html', {'form': form} | common_context(request, org_id))

@login_required
def organization_create(request):
    return organization_edit(request, 0)

@login_required
def account_list(request, org_id):
    if not check_org_access(request, org_id):
        return redirect('organization_list_url') 

    account_list_data = account.objects.filter(organization=org_id)

    account_type_choices = account._meta.get_field('account_type').choices    
    return render(request, 'azbooks/account_list.html', {'account_list_data': account_list_data, 'account_type_choices': account_type_choices } | common_context(request, org_id))

@login_required
# account_edit will be a api call to create or update account
def account_edit(request, org_id, pk):
    if not check_org_access(request, org_id):
        return JsonResponse({'error': 'You do not have access to this organization.'}, status=403) 

    if request.method == 'POST':
        request_body = request.body.decode('utf-8')
        request_body = json.loads(request_body)

        print(request_body)

        if pk == 0:
            form = accountForm(request_body)
            print(form)
        else:
            account.objects.filter(pk=pk).update(                
                name=request_body['coa_name'],
                account_type=request_body['coa_type'],
                code=request_body['coa_code']
            )
            
            account_obj = account.objects.filter(pk=pk).first()
            return JsonResponse(
                {
                    'status': 'success', 
                    'account_id': pk, 
                    'message': 'Account updated successfully.',
                    'coa_name': account_obj.name,
                    'coa_type': account_obj.account_type,
                    'coa_code': account_obj.code
                    
                }, 
                    status=200
            )


            


    else:
        if pk == 0:
            form = accountForm()
        else:
            account_obj = account.objects.get(pk=pk)
            form = accountForm(instance=account_obj)
    


    return render(request, 'azbooks/account_form.html', {'form': form} | common_context(request, org_id))


@login_required
def party_list(request, org_id=None):
    if not check_org_access(request, org_id):
        return redirect('organization_list_url') 
    
    party_list_data = party.objects.filter(organization=org_id)
    
    return render(request, 'azbooks/party_list.html', {'party_list_data': party_list_data} | common_context(request, org_id))

@login_required
def party_edit(request, pk=None, org_id=None):
    if not check_org_access(request, org_id):
        return redirect('organization_list_url') 
    
    if pk:
        party_obj = party.objects.get(pk=pk)
        print(party_obj)
    else:
        party_obj = None

    if request.method == 'POST':
        form = partyForm(request.POST, instance=party)
        if form.is_valid():
            form.save()
            return redirect('party_list_url', org_id=1)
    else:
        form = partyForm(instance=party_obj)
    return render(request, 'azbooks/party_form.html', {'form': form} | common_context(request, org_id))


@login_required
def transaction_list(request, org_id=None):
    if not check_org_access(request, org_id):
        return redirect('organization_list_url') 
    
    transaction_list_data = transaction_header.objects.filter(organization=org_id)
    
    return render(request, 'azbooks/transaction_ledger_list.html', {'transaction_list_data': transaction_list_data} | common_context(request, org_id))