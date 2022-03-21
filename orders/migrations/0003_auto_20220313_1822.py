# Generated by Django 3.1.3 on 2022-03-13 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_user'),
        ('orders', '0002_remove_order_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='product_name',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='products.product'),
        ),
    ]
