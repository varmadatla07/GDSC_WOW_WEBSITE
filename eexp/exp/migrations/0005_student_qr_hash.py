# Generated by Django 4.0.6 on 2023-03-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exp', '0004_student_razor_pay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='qr_hash',
            field=models.CharField(blank=True, max_length=228, null=True),
        ),
    ]
