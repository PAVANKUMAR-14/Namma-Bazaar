from django.contrib import admin
from accounts.models import Accounts, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.

class Accountadmin (UserAdmin):
    list_display=['email','first_name','last_name','username','date_joined','last_login','is_active',]
    list_display_links=['email','first_name','last_name']
    readonly_fields=['date_joined','last_login']
    ordering=['-date_joined']

    #these fields are required by deafault when we create custom admin panel
    list_filter=()
    filter_horizontal=()
    fieldsets=()

admin.site.register(Accounts,Accountadmin)

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail (self, object):
        return format_html ('<img src="{}" style="border-radius:20%" width="30">'. format(object.profile_picture.url))
    thumbnail.short_description= 'profile picture'
    list_display=['thumbnail','user','city','state','country']

admin.site.register(UserProfile, UserProfileAdmin)
