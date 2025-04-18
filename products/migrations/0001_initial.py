# Generated by Django 5.1.6 on 2025-04-15 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productCollections', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.TextField()),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=6)),
                ('condition', models.CharField(choices=[('new', 'New'), ('excellent', 'Excellent'), ('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], max_length=20)),
                ('category', models.CharField(choices=[('ball', 'Ball Sports'), ('racket', 'Racket Sports'), ('fitness', 'Fitness Equipment'), ('indoor', 'indoor Sports'), ('water', 'Water Sports'), ('winter', 'Winter Sports'), ('extreme', 'extreme Sports')], max_length=20)),
                ('brand', models.CharField(max_length=50)),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.FileField(upload_to='media/')),
                ('status', models.CharField(choices=[('available', 'Available'), ('unavailable', 'unavailable')], default='available', max_length=20)),
                ('collections', models.ManyToManyField(blank=True, related_name='equipment', to='productCollections.collection')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_date', models.DateTimeField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.equipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.equipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Borrow_Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.equipment')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('equipment', 'user'), name='request_only_once')],
            },
        ),
    ]
