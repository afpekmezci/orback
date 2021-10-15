# Generated by Django 3.2.8 on 2021-10-12 07:16

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=120, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=64, verbose_name='İsim')),
                ('is_first', models.BooleanField(default=True, verbose_name='is first')),
                ('person_image', models.ImageField(blank=True, null=True, upload_to=core.utils.get_upload_path)),
                ('person_thumbnail', models.ImageField(blank=True, null=True, upload_to=core.utils.get_upload_path)),
                ('is_public', models.BooleanField(default=False, verbose_name='Başkaları tarafından görüntülenebilir mi?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('invited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_invited_by', to=settings.AUTH_USER_MODEL, verbose_name='Davet Eden')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ForgetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('forget_code', models.CharField(max_length=128, verbose_name='Davet kodu')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forget_password', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
