# Generated by Django 4.1.5 on 2023-02-27 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_employee_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='father_name',
        ),
    ]
