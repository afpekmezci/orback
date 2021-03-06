# Generated by Django 3.2.8 on 2021-10-12 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=1024, verbose_name='Hospital')),
                ('city', models.CharField(max_length=128, verbose_name='City')),
                ('town', models.CharField(blank=True, max_length=128, null=True, verbose_name='Town')),
                ('hospital_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='Type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=128, verbose_name='Warehouse Name')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='City')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouses', to='organization.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
