# Generated by Django 4.2 on 2024-12-04 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictar', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guide',
            options={'verbose_name': 'Tour Guide', 'verbose_name_plural': 'Tour Guides'},
        ),
        migrations.RemoveField(
            model_name='guide',
            name='created_date',
        ),
        migrations.AddField(
            model_name='guide',
            name='experience',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='guide',
            name='languages_spoken',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='guide',
            name='designation',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='guide',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='guide',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='guide',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='tour_guides_photos/'),
        ),
    ]
