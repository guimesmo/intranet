# Generated by Django 2.0.7 on 2018-07-25 02:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import file_manager.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public', models.BooleanField(default=False, verbose_name='público')),
                ('upload', models.FileField(upload_to=file_manager.models.user_directory_path)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='responsável')),
            ],
        ),
    ]
