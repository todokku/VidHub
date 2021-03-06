# Generated by Django 3.0.1 on 2019-12-26 01:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import video_encoding.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('channel_id', models.CharField(blank=True, max_length=10)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch_id', models.CharField(blank=True, max_length=10)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('public', 'public'), ('private', 'private'), ('unlisted', 'unlisted'), ('drafting', 'drafting')], max_length=8)),
                ('view_count', models.BigIntegerField(default=0)),
                ('video_type', models.CharField(choices=[('local', 'Local file'), ('remote', 'Remote file'), ('embed', 'From YouTube')], default='local', max_length=10)),
                ('uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('width', models.PositiveIntegerField(editable=False, null=True)),
                ('height', models.PositiveIntegerField(editable=False, null=True)),
                ('duration', models.FloatField(editable=False, null=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='thumbnails/')),
                ('file', video_encoding.fields.VideoField(height_field='height', upload_to='', width_field='width')),
                ('processed', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streamer.Category')),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='streamer.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to='streamer.Channel')),
                ('to_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Channel')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Channel')),
                ('videos', models.ManyToManyField(to='streamer.PlaylistEntry')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Dislikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Video')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='streamer.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='streamer.Video')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
