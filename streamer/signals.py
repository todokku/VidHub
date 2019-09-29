import random
import string
import os

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django_rq import enqueue

from video_encoding import tasks

from .models import Video
from .models import Profile
from .models import Channel

@receiver(post_save, sender=Video)
def convert_video(sender, instance, created, **kwargs):
	if created:
		enqueue(tasks.convert_all_videos,
				instance._meta.app_label,
				instance._meta.model_name,
				instance.pk)


def generate_id(length):
	chars = string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for _ in range(length))

@receiver(pre_save, sender=Video)
def pre_save_create_watch_id(sender, instance, **kwargs):
	if not instance.watch_id:
		new_watch_id = generate_id(8)
		while sender.objects.filter(watch_id=new_watch_id).exists():
			new_watch_id = generate_id(8)
		instance.watch_id = new_watch_id

@receiver(pre_save, sender=Channel)
def pre_save_create_channel_id(sender, instance, **kwargs):
	if not instance.channel_id:
		new_channel_id = generate_id(8)
		while sender.objects.filter(channel_id=new_channel_id).exists():
			new_channel_id = generate_id(8)
		instance.channel_id = new_channel_id

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()