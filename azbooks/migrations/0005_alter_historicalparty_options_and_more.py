# Generated by Django 4.1.2 on 2022-10-12 19:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('azbooks', '0004_remove_historicalcountry_base_currency_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalparty',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical party', 'verbose_name_plural': 'historical parties'},
        ),
        migrations.AlterModelOptions(
            name='historicaltransaction_detail',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical transaction line', 'verbose_name_plural': 'historical transaction details'},
        ),
        migrations.AlterModelOptions(
            name='historicaltransaction_header',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical transaction', 'verbose_name_plural': 'historical transaction ledger'},
        ),
        migrations.AlterModelOptions(
            name='party',
            options={'verbose_name': 'party', 'verbose_name_plural': 'parties'},
        ),
        migrations.AlterModelOptions(
            name='transaction_detail',
            options={'verbose_name': 'transaction line', 'verbose_name_plural': 'transaction details'},
        ),
        migrations.AlterModelOptions(
            name='transaction_header',
            options={'verbose_name': 'transaction', 'verbose_name_plural': 'transaction ledger'},
        ),
        migrations.AlterField(
            model_name='historicaltransaction_header',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='transaction_header',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
