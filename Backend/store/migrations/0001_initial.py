# Generated by Django 5.0.1 on 2024-08-10 15:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('branch_code', models.CharField(blank=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('contact_details', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DamageProductTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('damage_transfer_number', models.CharField(max_length=100, unique=True)),
                ('total_qty_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='ProductInTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('supplier_invoice_number', models.CharField(max_length=100, unique=True)),
                ('total_qty_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TotalStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=100, unique=True)),
                ('total_quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('purchase_date', models.DateField()),
                ('unit', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('expiry_date', models.DateField()),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('manufacturing_date', models.DateField()),
                ('product_code', models.CharField(max_length=100)),
                ('barcode', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='DamageProductTransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('total', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('remarks', models.TextField(blank=True, null=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='store.damageproducttransaction')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='damage_transaction_details', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInTransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('total', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('remarks', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_transaction_details', to='store.product')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='store.productintransaction')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOutTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('branch_incharge', models.CharField(max_length=255)),
                ('supplier_invoice_number', models.CharField(max_length=100, unique=True)),
                ('total_qty_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_transactions', to='store.branch')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOutTransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('total', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('remarks', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_transaction_details', to='store.product')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='store.productouttransaction')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('order_form_number', models.CharField(max_length=100, unique=True)),
                ('branch_incharge', models.CharField(max_length=255)),
                ('total_qty_amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_requests', to='store.branch')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseRequestDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('total', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('remarks', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_request_details', to='store.product')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='store.purchaserequest')),
            ],
        ),
        migrations.AddField(
            model_name='productintransaction',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_transactions', to='store.supplier'),
        ),
    ]
