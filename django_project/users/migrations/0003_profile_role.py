# Generated migration for adding role field to Profile model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('buyer', 'Buyer'), ('requester', 'Requester')], default='requester', max_length=20),
        ),
    ]
