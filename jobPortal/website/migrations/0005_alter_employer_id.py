# Generated by Django 4.2.7 on 2023-12-12 13:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_employer_company_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
