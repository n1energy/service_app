# Generated by Django 3.2.16 on 2023-02-03 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_subscription_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='description',
            field=models.CharField(blank=True, db_index=True, default='', max_length=50),
        ),
    ]
