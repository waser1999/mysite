from django.contrib import admin

# Register your models here.
from .models import info, userInfo, idata

admin.site.register(info)
admin.site.register(userInfo)
admin.site.register(idata)