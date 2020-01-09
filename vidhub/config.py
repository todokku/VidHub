class Config:
	SECRET_KEY = '4p#&7+l#ws*s^rm(o&qh0ph6h3p*n2wdmkmy2i&#q$5jtkm1m5'
	ALLOWED_HOSTS = ['vidhub']
	ROOT_URLCONF = 'vidhub.urls'
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'kqsl1y8xgdzqc6vr',
			'USER': 'c3s3dvgzh10510r2',
			'PASSWORD': 'hxlievnpt2hu4iw8',
			'HOST': 'p2d0untihotgr5f6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
			'PORT': '3306',
		}
	}
	MAINTENANCE_MODE = None
	MAINTENANCE_MODE_TEMPLATE = 'streamer/maintenance.html'
	MAINTENANCE_MODE_IGNORE_ADMIN_SITE = False
	MAINTENANCE_MODE_IGNORE_AUTHENTICATED_USER = False
	DEBUG = True
