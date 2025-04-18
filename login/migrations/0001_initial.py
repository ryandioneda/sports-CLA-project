# Generated by Django 5.1.6 on 2025-04-15 17:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPerms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('borrower_perms', 'Global borrower permissions'), ('lender_perms', 'Global lender permissions')),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=64, null=True)),
                ('lname', models.CharField(max_length=64, null=True)),
                ('birth_date', models.DateField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.CharField(max_length=128, null=True)),
                ('city', models.CharField(max_length=64, null=True)),
                ('state', models.CharField(max_length=5, null=True)),
                ('zip_code', models.CharField(max_length=5, null=True)),
                ('image', models.FileField(upload_to='media/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
