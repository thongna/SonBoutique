# Generated by Django 2.1 on 2018-08-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20180819_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='pay_by',
            field=models.CharField(choices=[('1', 'cash'), ('2', 'bank transfer'), ('3', 'credit card'), ('4', 'paypal')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=12),
            preserve_default=False,
        ),
    ]
