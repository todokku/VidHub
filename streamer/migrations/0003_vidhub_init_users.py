# Generated by Django 2.2.2 on 2019-07-19 15:42

from django.db import migrations
from django.contrib.auth.hashers import make_password


def init_users(apps, schema_editor):
	User = apps.get_model('auth', 'User')
	Channel = apps.get_model('streamer', 'Channel')
	Profile = apps.get_model('streamer', 'Profile')
	data = [
		('john', 'John'),
		('bob', 'Bob'),
		('vidhub', 'Offical Vidhub'),
	]

	for username, channelname in data:
		user = User.objects.create(username=username, password=make_password('sommer', None, 'md5'))
		Profile.objects.create(user=user)
		Channel.objects.create(name=channelname, owner=user)


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0002_vidhub_init_categories'),
    ]

    operations = [
    	migrations.RunPython(init_users),
    ]