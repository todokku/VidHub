import os

from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.vary import vary_on_headers
from django.forms.models import model_to_dict
from django.core.files.images import ImageFile
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from video_encoding.backends.ffmpeg import FFmpegBackend

from .models import Video, Channel, Category, Playlist, PlaylistEntry, Subscription, Likes
from .forms import VideoForm, EditVideoForm, SignUpForm, LoginForm

def index(request):
	categories = Category.objects.all()
	search=request.GET.get('q', None)
	category_name = request.GET.get('c', None)
	if category_name:
		category = Category.objects.get(name__exact=category_name)
		videos = Video.objects.filter(category__exact=category)
	else:
		videos = Video.objects.all()
	if search:
		videos = videos.filter(title__icontains=search)
	context = { 'videos' : videos, 'categories' : categories }
	if request.user.is_authenticated:
		context['channel'] = Channel.objects.get(owner__exact=request.user)
	return render(request, 'streamer/index.html', context)

def video(request, watch_id):
	video = get_object_or_404(Video, watch_id__exact=watch_id)
	video.view_count += 1
	video.save()
	like_count = Likes.objects.filter(video__exact=video).count()
	is_video_liked = False
	if request.user.is_authenticated:
		channel = Channel.objects.get(owner__exact=request.user)
		playlist = Playlist.objects.get(owner__exact=channel, title__exact='History')
		playlistEntry = PlaylistEntry.objects.create(video=video)
		playlist.videos.add(playlistEntry)
		is_video_liked = Likes.objects.filter(user__exact=request.user, video__exact=video).exists()
	formats = video.format_set.complete().all()
	for e in formats:
		e.codec,e.label = e.format.split('_')
		print(e.codec)
		print(e.label)
	return render(request, 'streamer/video.html', {'video' : video, 'formats' : formats, 'is_video_liked' : is_video_liked, 'like_count' : like_count})

@login_required
def uploadVideo(request):
	if request.method == 'POST':
		if request.is_ajax():
			if request.POST.get('get_thumbnail'):
				video = Video.objects.get(watch_id__exact=request.POST.get('watch_id'))
				response = {'thumbnails' : []}
				for i in list(range(3)):
					timestamp = min(((video.duration / 3) / 0.5) + i, video.duration-0.5)
					tmp_thumbnail = FFmpegBackend().get_thumbnail(video_path=video.file.path, at_time=timestamp)
					filename = 'thumbnail_{}_{}.jpg'.format(video.watch_id, i)
					server_path = os.path.join(settings.MEDIA_ROOT, filename)
					os.rename(tmp_thumbnail, server_path)
					url = settings.MEDIA_URL + filename
					response['thumbnails'].append(url)
				print(response)
				return JsonResponse(response)
			else:
				form = VideoForm(request.POST, request.FILES)
				if form.is_valid():
					video = form.save()
					video.channel = Channel.objects.get(owner__exact=request.user.id)
					video.save()
					data = {'is_valid' : True, 'name' : video.file.name, 'url' : video.file.url, 'watch_id' : video.watch_id}
				else:
					data = {'is_valid' : False}	
				return JsonResponse(data)
		else:
			video = Video.objects.get(watch_id__exact=request.POST.get('watch_id', ''))
			print(request.POST, request.FILES)
			if request.POST.get('selected_thumbnail') == "custom":
				pass
			else:
				filename = os.path.basename(request.POST.get('selected_thumbnail'))
				print(filename)
				full_path = os.path.join(settings.MEDIA_ROOT, filename) 
				print(full_path)
				f = open(full_path, 'rb')
				video.thumbnail.save(filename, ImageFile(f), save=False)
				f.close()
			video.title = request.POST.get('title')
			video.description = request.POST.get('description')
			video.save()
			return redirect("/")
	else:
		form = VideoForm()
		return render(request, 'streamer/upload.html', {'form' : form, 'initial_upload' : True})

def editVideo(request, watch_id):
	video = get_object_or_404(Video, watch_id__exact=watch_id)
	if request.method == 'POST':
		form = EditVideoForm(request.POST, request.FILES or None, instance=video)
		if form.is_valid():
			form.save()
	form = EditVideoForm(instance=video)
	return render(request, 'streamer/edit_video.html', {'form' : form})

def login(request):
	print(request)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid:
			print(request.POST)
			user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
			if user is not None:
				login(user)
				return redirect('/')
	else:
		form = LoginForm()
	return render(request, 'streamer/login.html', {'form' : form})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid:
			user = form.save()
			user.refresh_from_db()
			user.save()
			channel = Channel.objects.create(name=request.POST.get('channel_name'), owner=user)
			channel.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'streamer/signup.html', {'form' : form})

def channel(request, channel_id):
	channel = Channel.objects.get(channel_id__exact=channel_id)
	videos = Video.objects.filter(channel__exact=channel)

	if request.user.is_authenticated:
		loggedin_channel = Channel.objects.get(owner__exact=request.user)
		subscribed = Subscription.objects.filter(from_channel__exact=loggedin_channel, to_channel__exact=channel).exists()
	else:
		subscribed = False
	return render(request, 'streamer/channel.html', {'channel' : channel, 'videos' : videos, 'subscribed' : subscribed})

@login_required
def history(request):
	channel = Channel.objects.get(owner__exact=request.user.id)
	playlist = Playlist.objects.get(owner__exact=channel, title__exact='History')
	videos = playlist.videos.order_by('-date_added')
	return render(request, 'streamer/history.html', { 'videos' : videos })

def subscribe(request):
	if request.method == 'POST' and request.user.is_authenticated:
		from_channel = Channel.objects.get(owner__exact=request.user)
		to_channel = Channel.objects.get(pk=request.POST.get('channel_id'))

		if request.POST.get('action') == 'subscribe':
			Subscription.objects.create(from_channel=from_channel, to_channel=to_channel)
		else:
			subscription = Subscription.objects.get(from_channel__exact=from_channel, to_channel__exact=to_channel)
			subscription.delete()
		return JsonResponse({'success' : True})
	else:
		raise SuspiciousOperation

def like(request):
	if request.method == 'POST' and request.user.is_authenticated:
		video = Video.objects.get(pk=request.POST.get('video_id'))
		
		if request.POST.get('action') == 'like':
			if not Likes.objects.filter(user__exact=request.user, video__exact=video).exists():
				Likes.objects.create(video=video, user=request.user)
		
		elif request.POST.get('action') == 'unlike':
			Likes.objects.filter(user__exact=request.user, video__exact=video).delete();

		like_count = Likes.objects.filter(video__exact=video).count()
		return JsonResponse({'success' : True, 'like_count' : like_count})
	else:
		raise SuspiciousOperation