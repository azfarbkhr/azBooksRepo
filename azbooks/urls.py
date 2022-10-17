from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('register', views.register_request, name="register"),
    path('favicon.ico',RedirectView.as_view(url=staticfiles_storage.url("azbooks/images/favicon.png"))),
    path('', views.organization_list, name="organization_list_url"),
    path('org/list', views.organization_list, name="organization_list_url"),
    path('org/edit/<int:org_id>', views.organization_edit, name="organization_edit_url"),
    path('org/create', views.organization_create, name="organization_create_url"),
    path('org/<int:org_id>/account/list', views.account_list, name='account_list_url'),
    path('org/<int:org_id>/account/edit/<int:pk>', views.account_edit, name='account_edit_url'),
    path('org/<int:org_id>/account/create', views.account_edit, name='account_create_url'),
    path('org/<int:org_id>/party/list', views.party_list, name='party_list_url'),
    path('org/<int:org_id>/party/edit/<int:pk>', views.party_edit, name='party_edit_url'),
    path('org/<int:org_id>/party/create', views.party_edit, name='party_create_url'),
    path('org/<int:org_id>/transaction/list', views.transaction_list, name='transaction_list_url'),

]