from django.contrib import admin
from apps.home.models import Contact, Subscribe,  Favourite
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    search_fields = ['name', 'email']
    list_filter = ['created_at']
    
@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']
    list_filter = ['created_at']

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'resource_id','user', 'resource']
    search_fields = ['user__username', 'resource__title']
    list_filter = ['created_at']