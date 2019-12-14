# from datetime import date, datetime
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from video_encoding.fields import VideoField
from video_encoding.models import Format

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class Channel(models.Model):
	name = models.CharField(max_length=100)
	owner = models.OneToOneField(User, on_delete=models.CASCADE)
	channel_id = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.name

class Category(models.Model):
	title = models.CharField(max_length=100)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.title

class Video(models.Model):
	VIDEO_STATUS_CHOICES = (
		('public', 'public'),
		('private', 'private'),
		('unlisted', 'unlisted'),
	)

	VIDEO_TYPE_CHOICES = (
		('local', 'Local file'),
		('remote', 'Remote file'),
		('embed', 'From YouTube'),
	)

	watch_id = models.CharField(max_length=10, blank=True)
	title = models.CharField(max_length=100, blank=True)
	description = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=8, choices=VIDEO_STATUS_CHOICES, blank=True)
	view_count = models.BigIntegerField(default=0)
	video_type = models.CharField(max_length=10, choices=VIDEO_TYPE_CHOICES, default='local')
	uploaded = models.DateTimeField(default=timezone.now)
	width = models.PositiveIntegerField(editable=False, null=True)
	height = models.PositiveIntegerField(editable=False, null=True)
	duration = models.FloatField(editable=False, null=True)
	thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
	file = VideoField(width_field='width', height_field='height', duration_field='duration')
	format_set = GenericRelation(Format)

	channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return str(self.file)

	def get_channel(self):
		return Channel.objects.get(pk__exact=self.channel)

class PlaylistEntry(models.Model):
	video = models.ForeignKey(Video, on_delete=models.CASCADE)
	date_added = models.DateTimeField(default=timezone.now)

class Playlist(models.Model):
	title = models.CharField(max_length=100)
	owner = models.ForeignKey(Channel, on_delete=models.CASCADE)
	videos = models.ManyToManyField(PlaylistEntry)

	def __str__(self):
		return self.title


class Subscription(models.Model):
	from_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="subscriber")
	to_channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, on_delete=models.CASCADE)

class Dislikes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, on_delete=models.CASCADE)