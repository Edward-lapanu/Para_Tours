# Generated by Django 4.2 on 2024-12-05 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(default='resorts/default.jpg', upload_to='resorts/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resorts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('resort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perl_app.resort')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
