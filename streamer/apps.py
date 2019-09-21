from django.apps import AppConfig

class StreamerConfig(AppConfig):
    name = 'streamer'
    label = 'streamer'

    def ready(self):
    	import streamer.signals