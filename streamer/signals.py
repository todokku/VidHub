import random
import string
import os
import magic

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from django_rq import enqueue

from video_encoding import tasks

from .models import Video, Channel, Playlist

@receiver(post_save, sender=Video)
def convert_video(sender, instance, created, **kwargs):
	if created:
		f = os.path.join(settings.MEDIA_ROOT, instance.file.name)
		if not magic.from_file(f, mime=True).startswith('video/'):
			instance.delete()
		else:
			enqueue(tasks.convert_all_videos,
					instance._meta.app_label,
					instance._meta.model_name,
					instance.pk)

@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance, **kwargs):
	if instance.file:
		if os.path.isfile(instance.file.path):
			os.remove(instance.file.path)
	for f in instance.format_set.all():
		if f.file:
			if os.path.isfile(f.file.path):
				os.remove(f.file.path)
	if instance.thumbnail:
		if os.path.isfile(instance.thumbnail.path):
			os.remove(instance.thumbnail.path)

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

@receiver(tasks.video_convert_done)
def on_video_convert_done(video, **kwargs):
	video.processed = True
	video.save()

	