# Generated by Django 3.2.8 on 2021-10-09 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='organizations',
        ),
        migrations.AddField(
            model_name='hospital',
            name='city',
            field=models.CharField(default=1, max_length=128, verbose_name='City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='hospital_type',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Type'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='town',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Town'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Hospital'),
        ),
    ]
