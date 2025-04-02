from django.contrib import admin
from apps.formula.models import Formula, FunksionalData
# import html safe
from django.utils.safestring import mark_safe
    
@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'variables', 'get_formula', 'get_code', ]
    list_display_links = ['name']
    search_fields = ['name', 'variables', 'code']
    list_filter = ['name', 'variables', 'code']
    readonly_fields = ['variables', 'formula_img']
    list_per_page = 10
    list_max_show_all = 100
    
    
    def get_code(self, obj):
        return mark_safe(f"<pre>{obj.code}</pre>")
    
    
@admin.register(FunksionalData)
class FunksionalDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file', ]
    list_display_links = ['name']
    search_fields = ['name', 'file']
    list_filter = ['name', 'file']
    list_per_page = 10
    list_max_show_all = 100