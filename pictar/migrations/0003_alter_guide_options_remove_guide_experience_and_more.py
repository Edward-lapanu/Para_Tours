# Generated by Django 4.2 on 2024-12-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictar', '0002_alter_guide_options_remove_guide_created_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guide',
            options={},
        ),
        migrations.RemoveField(
            model_name='guide',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='guide',
            name='languages_spoken',
        ),
        migrations.AddField(
            model_name='guide',
            name='created_date',
            field=models.DateTimeField(null='True'),
            preserve_default='True',
        ),
        migrations.AlterField(
            model_name='guide',
            name='designation',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='guide',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='guide',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='guide',
            name='photo',
            field=models.ImageField(upload_to='photos/%y/%m/%d/'),
        ),
    ]
