# Generated by Django 3.2.8 on 2021-10-09 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0002_auto_20211008_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationuser',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_organizatons', to='organization.organization'),
        ),
        migrations.AlterField(
            model_name='organizationuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_user', to=settings.AUTH_USER_MODEL),
        ),
    ]