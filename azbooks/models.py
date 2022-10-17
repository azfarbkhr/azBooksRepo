from email.policy import default
from operator import mod
from random import choices
from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
import pycountry
import datetime 

class organization(models.Model):
    name = models.CharField(max_length=500)
    country = models.CharField(max_length=100, choices=[(country.name, country.name) for country in pycountry.countries], blank=True, null=True)
    currency = models.CharField(max_length=100, choices=[(currency.name, currency.name) for currency in pycountry.currencies], blank=True, null=True )
    access_users = models.ManyToManyField(User, through='user_organization_access')
    phone = models.CharField(max_length=100, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "organizations"
        verbose_name = "organization"

    def get_users(self):
        return ", ".join([u.email or u.username for u in self.access_users.all()])

    



class user_organization_access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username + " | " + self.organization.name

    class Meta:
        verbose_name_plural = "user organization access"
        verbose_name = "user organization access"


class account(models.Model):
    class account_type(models.TextChoices):
        ASSET = 'Asset'
        LIABILITY = 'Liability'
        EQUITY = 'Equity'
        SALE = 'Sale'
        EXPENSE = 'Expense'

    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100, choices=account_type.choices)
    is_bank_account = models.BooleanField(default=False)
    is_sale_tax_account = models.BooleanField(default=False)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name + " " + self.account_type

    class Meta:
        verbose_name_plural = "chart of accounts"
        verbose_name = "account"

class party(models.Model):
    name = models.CharField(max_length=100)
    legal_company_name = models.CharField(max_length=100, blank=True, null=True)
    is_customer = models.BooleanField(default=False, blank=True, null=True)
    is_supplier = models.BooleanField(default=False, blank=True, null=True)
    is_employee = models.BooleanField(default=False, blank=True, null=True)
    is_bank = models.BooleanField(default=False, blank=True, null=True)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "parties"
        verbose_name = "party"


class transaction_header(models.Model):
    date = models.DateField(default= datetime.date.today) 
    reference = models.CharField(max_length=100, blank=True, null=True)
    folio_reference = models.CharField(max_length=100, blank=True, null=True)
    memo = models.TextField(max_length=1000, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    party = models.ForeignKey(party, on_delete=models.CASCADE, blank=True, null=True)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id) + " (" + self.date.strftime('%d-%b-%y') + " | " + (self.reference or "No Reference") + " | " + self.party.name + ")"

    def total_credit(self):
        return sum([t.credit_amount for t in self.details.all() if t.credit_amount])

    def total_debit(self):
        return sum([t.debit_amount for t in self.details.all() if t.debit_amount])

    class Meta:
        verbose_name_plural = "transaction ledger"
        verbose_name = "transaction"


class transaction_detail(models.Model):
    transaction_header = models.ForeignKey(transaction_header, on_delete=models.CASCADE, related_name='details')
    account = models.ForeignKey(account, on_delete=models.CASCADE)
    debit_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    credit_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.id) + " (" +  self.account.name + " | " + (self.transaction_header.reference or "No Reference")  +  " | " + self.transaction_header.date.strftime('%d-%b-%y') + ")"

    class Meta:
        verbose_name_plural = "transaction details"
        verbose_name = "transaction line"
        # constraint that debit and credit both can not be present
        constraints = [
            models.CheckConstraint(check=models.Q(debit_amount__isnull=False) | models.Q(credit_amount__isnull=False), name='debit_or_credit', violation_error_message='Either debit or credit amount must be present'),
            models.CheckConstraint(check=~models.Q(debit_amount__isnull=False) | ~models.Q(credit_amount__isnull=False), name='debit_and_credit', violation_error_message='Both debit and credit amount can not be present'),
            models.CheckConstraint(check=models.Q(debit_amount__isnull=True) | models.Q(debit_amount__gt=0), name='debit_amount_positive', violation_error_message='Debit amount must be positive'),
            models.CheckConstraint(check=models.Q(credit_amount__isnull=True) | models.Q(credit_amount__gt=0), name='credit_amount_positive', violation_error_message='Credit amount must be positive'),
        ]




