# Generated by Django 4.1.2 on 2022-10-12 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('azbooks', '0006_alter_historicaltransaction_detail_credit_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaltestmodel',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='testModel',
        ),
        migrations.AlterField(
            model_name='transaction_detail',
            name='transaction_header',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='azbooks.transaction_header'),
        ),
        migrations.AddConstraint(
            model_name='transaction_detail',
            constraint=models.CheckConstraint(check=models.Q(('debit_amount__isnull', False), ('credit_amount__isnull', False), _connector='OR'), name='debit_or_credit', violation_error_message='Either debit or credit amount must be present'),
        ),
        migrations.AddConstraint(
            model_name='transaction_detail',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('debit_amount__isnull', False), _negated=True), models.Q(('credit_amount__isnull', False), _negated=True), _connector='OR'), name='debit_and_credit', violation_error_message='Both debit and credit amount can not be present'),
        ),
        migrations.AddConstraint(
            model_name='transaction_detail',
            constraint=models.CheckConstraint(check=models.Q(('debit_amount__isnull', True), ('debit_amount__gt', 0), _connector='OR'), name='debit_amount_positive', violation_error_message='Debit amount must be positive'),
        ),
        migrations.AddConstraint(
            model_name='transaction_detail',
            constraint=models.CheckConstraint(check=models.Q(('credit_amount__isnull', True), ('credit_amount__gt', 0), _connector='OR'), name='credit_amount_positive', violation_error_message='Credit amount must be positive'),
        ),
        migrations.DeleteModel(
            name='HistoricaltestModel',
        ),
    ]
