# Generated by Django 4.1.5 on 2023-02-27 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_employee_father_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='state',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
