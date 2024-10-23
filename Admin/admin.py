from django.contrib import admin
from .models import Brand, Banner, BannerGroup
# Register your models here.

admin.site.register(Brand)
admin.site.register(Banner)
admin.site.register(BannerGroup)