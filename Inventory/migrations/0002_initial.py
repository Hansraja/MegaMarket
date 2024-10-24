# Generated by Django 5.1.2 on 2024-10-19 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Inventory', '0001_initial'),
        ('User', '0001_initial'),
        ('Vendor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Vendor.vendor'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.item'),
        ),
        migrations.AddField(
            model_name='itemreview',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.item'),
        ),
        migrations.AddField(
            model_name='itemreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='itemvariation',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='Inventory.item'),
        ),
        migrations.AddField(
            model_name='itemreview',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.itemvariation'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.itemvariation'),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='User.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='User.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.item'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.itemvariation'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(related_name='item_tags', to='Inventory.tag'),
        ),
        migrations.AlterUniqueTogether(
            name='itemvariation',
            unique_together={('item', 'name', 'value')},
        ),
        migrations.AlterUniqueTogether(
            name='itemreview',
            unique_together={('item', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('item', 'variant')},
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'item', 'variant')},
        ),
    ]
