# Generated by Django 4.2.7 on 2023-12-12 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_jobposting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='application_deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]