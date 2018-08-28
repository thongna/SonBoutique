# Generated by Django 2.0.5 on 2018-08-19 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_pay_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pay_by',
            field=models.CharField(choices=[('1', 'cash'), ('2', 'bank transfer'), ('3', 'credit card'), ('4', 'paypal')], default='1', max_length=1),
        ),
    ]
