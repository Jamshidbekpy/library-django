from django.db import models
from apps.common.models import BaseModel
from django.utils.text import slugify
from apps.resources.utils import add_watermark
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
# Create your models here.

RESOURCES_AUDITORIA = (
    ('all', 'Barcha uchun'),
    ('students', 'O\'quvchilar uchun'),
    ('teachers', 'O\'qituvchilar uchun')
)

RESOURCE_STATUS = (
    ('free', 'Bepul'),
    ('partial', 'Qisman ochiq'),
    ('premium', 'Premium')
    
)


class ResourceType(BaseModel):
    name = models.CharField(max_length=30, verbose_name='Resurs turi')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Resurs turi'
        verbose_name_plural = 'Resurslar turi'
        

class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name='kategoriya')
    slug = models.SlugField(default="", null=False)
    icon = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)   
        super(Category, self).save(*args, **kwargs)
             
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        

class Language(BaseModel):
    name = models.CharField(max_length=30, verbose_name='Til')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Til'
        verbose_name_plural = 'Tillar'


class Resource(BaseModel):
    photo = models.ImageField(upload_to='resources/', verbose_name='Rasm', null=True, blank=True)
    original_file = models.FileField(upload_to='pdfs/originals/', verbose_name='Fayl yuklash', 
                                     validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    watermarked_file = models.FileField(upload_to='pdfs/watermarkeds/', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Sarlavha')
    description = models.TextField(verbose_name='Tavsif')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=100, verbose_name='Muallif', null=True, blank=True)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.SET_NULL, null=True, verbose_name='Resurs turi', related_name='resurslar')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, verbose_name='Til')
    country = models.CharField(max_length=30, verbose_name='Mamlakat', null=True, blank=True)
    year = models.PositiveIntegerField(verbose_name='Yil', null=True, blank=True)
    direction = models.CharField(max_length=100, verbose_name='Yo\'nalish', null=True, blank=True)
    pages = models.PositiveIntegerField(verbose_name='Sahifalar soni', null=True, blank=True)
    keywords = models.CharField(max_length=255, verbose_name='Kalit so\'zlar', null=True, blank=True)
    auditoria = models.CharField(max_length=30, choices=RESOURCES_AUDITORIA, default='all', verbose_name='Ruxsat')
    status = models.CharField(max_length=30, choices=RESOURCE_STATUS, default='free', verbose_name='Holat')
    slug = models.SlugField(default="", null=False)
    views = models.PositiveIntegerField(default=0, verbose_name='Ko\'rishlar soni')

    @property
    def publish_year(self):
        if self.year:
            return self.year
        return ''
    

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)   
        super(Resource, self).save(*args, **kwargs)

        if self.original_file and not self.watermarked_file:
            watermarked_pdf = add_watermark(self.original_file, 'Salomatlik Maktabi')
            watermarked_content = ContentFile(watermarked_pdf.read())   
            self.watermarked_file.save(f"{self.original_file.name.split('/')[-1]}", watermarked_content)
    

    class Meta:
        verbose_name = 'Resurs'
        verbose_name_plural = 'Resurslar'
