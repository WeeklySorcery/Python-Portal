# Generated by Django 4.2.7 on 2023-12-11 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_employer_company_desc_employer_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='company_desc',
            field=models.CharField(blank=True, max_length=655, null=True),
        ),
    ]
