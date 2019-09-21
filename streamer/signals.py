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

@receiver(post_save, sender=Video)
def convert_video(sender, instance, created, **kwargs):
	if created:
		enqueue(tasks.convert_all_videos,
				instance._meta.app_label,
				instance._meta.model_name,
				instance.pk)


def generate_watch_id():
	chars = string.ascii_letters + string.digits
	length = 8
	return ''.join(random.choice(chars) for _ in range(length))

@receiver(pre_save, sender=Video)
def pre_save_create_watch_id(sender, instance, **kwargs):
	if not instance.watch_id:
		new_watch_id = generate_watch_id()
		while sender.objects.filter(watch_id=new_watch_id).exists():
			new_watch_id = generate_watch_id()
		instance.watch_id = new_watch_id


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()