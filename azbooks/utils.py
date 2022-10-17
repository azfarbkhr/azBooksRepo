from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *


# check user access and store value in session variable for future use
def check_org_access(request, org_id):
    accessible_org_ids = request.session.get('accessible_org_ids', None)

    if (not accessible_org_ids) or (org_id not in accessible_org_ids and org_id != -1):
        print('No accessible_org_ids in session. Getting from database.')
        orgs = user_organization_access.objects.filter(user=request.user)
        accessible_org_ids = list(org.organization_id for org in orgs)
        print(accessible_org_ids)
        request.session['accessible_org_ids'] = accessible_org_ids
    
    if org_id in accessible_org_ids or org_id == -1:
        return True
    else:
        messages.add_message(request, messages.WARNING, 'It seems you landed on an incorrect URL, please select relevant organization to resume.')
        return False


def get_org_name(request, org_id):
    org_name = request.session.get('org_name' + str(org_id), None)

    if not org_name:
        print('No org_name in session. Getting from database.')
        org_name = organization.objects.get(id=org_id).name
        request.session['org_name' + str(org_id)] = org_name
    
    return org_name

def common_context(request, org_id):
    org_name = get_org_name(request, org_id)
    return {'org_name': org_name, 'org_id': org_id}