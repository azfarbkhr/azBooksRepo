from dataclasses import field
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportMixin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget

from .models import *

admin.site.register(organization, SimpleHistoryAdmin,
    list_display = ['id', 'name', 'country', 'currency',  'phone', 'get_users'],
    list_filter = ['user_organization_access__user', ],
)

admin.site.register(user_organization_access, SimpleHistoryAdmin,
    list_display = ['user', 'organization'],
)

class account_resource(resources.ModelResource):
    organization = Field(attribute='organization', column_name='organization', widget=ForeignKeyWidget(organization, 'name'))
    class Meta:
        model = account
        exclude = ('id',)
        fields = ('code', 'name', 'account_type', 'organization', )
        export_order = ('code', 'name', 'account_type', 'organization', )
        import_id_fields = ['code', 'name', 'account_type', 'organization', ]
        report_skipped = True
        
class account_history_admin(SimpleHistoryAdmin):
    pass 

class account_admin(ImportExportMixin, account_history_admin):
    resource_class = account_resource


admin.site.register(account, account_admin,
    list_display = ['code', 'name', 'account_type', 'organization'],
    list_filter = ['account_type', 'organization'],
)

admin.site.register(party, SimpleHistoryAdmin,
    list_display = ['name', 'organization', 'legal_company_name', 'is_customer', 'is_supplier', 'is_employee', 'is_bank'],
    list_filter = ['organization', 'is_customer', 'is_supplier', 'is_employee', 'is_bank'],
)


# inline admin for tranasction detail
class transaction_detail_inline(admin.TabularInline):
    model = transaction_detail
    
    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        if obj:
            return 0
        return extra

admin.site.register(transaction_header, SimpleHistoryAdmin,
    list_display = ['date', 'reference', 'organization', 'party', 'memo'],
    list_filter = ['organization', 'party'],
    inlines = [transaction_detail_inline],
    fieldsets = (
        ('TRANSACTION HEADER', {
            'fields': (
                ('organization', 'total_amount', ),
                ('party', 'date', ),
                ('reference', 'folio_reference', ),
                ('memo', )
            )
        }),
    ),

)

admin.site.register(transaction_detail, SimpleHistoryAdmin,
    list_display = ['transaction_header', 'account', 'debit_amount', 'credit_amount'],
    list_filter = ['transaction_header', 'account'],
)
