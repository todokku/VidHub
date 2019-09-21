from django.contrib import admin

from video_encoding.admin import FormatInline

from .models import Video
from .models import Channel
from .models import Category

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
   inlines = (FormatInline,)

   list_dispaly = ('get_filename', 'width', 'height', 'duration')
   fields = ('file', 'width', 'height', 'duration')
   readonly_fields = fields

admin.site.register(Channel)
admin.site.register(Category)
