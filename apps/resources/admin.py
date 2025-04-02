from django.contrib import admin
from apps.resources.models import ResourceType, Resource, Language, Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    list_display_links=('id', 'name')
    readonly_fields = ('slug',)
    

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display=['id','name']
    list_display_links=['id','name']
    search_fields = ['name']
    

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display=['id', 'name']
    list_display_links=['id', 'name']
    search_fields=['name']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author','category', 'year', 'country', 'photo', 'language')
    list_display_links = ('id', 'title', 'author')
    search_fields = ('title', 'author', 'country', 'language__name' )
    readonly_fields = ('created_at', 'updated_at', 'slug', 'watermarked_file', 'views')
    list_filter = ('category', 'language')
    
