
from django.contrib import admin
from . import models
from .models import Item,RoomMember
# Register your models here.

# admin.site.register(Item)

@admin.register(models.Item)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('Name','Date', 'imageid','category','patientid', 'notes')
 

@admin.register(models.doctor)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('Name','docid')

admin.site.register(RoomMember)