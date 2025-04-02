from django.db import models
from ckeditor.fields import RichTextField
from apps.common.models import BaseModel
from apps.formula.utils import get_function_variables
from django.utils.text import slugify


CODE_DEFOULT = """# Agar qaysidir kutubxonadan foydalansangiz, ularni import qiling
def solution(a, b, c):
    # Siz o'zingizni formulangizni yozasiz
    
    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return "No real roots"
    
    x1 = (-b + (discriminant ** (1/2))) / (2*a)
    x2 = (-b - (discriminant ** (1/2))) / (2*a)
    
    return x1, x2
"""

FORMULA_DEFAULT = "x=(-b±√(b^2-4ac))/(2a)"



class Formula(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='Formula Name')
    image = models.ImageField(upload_to='formula/')
    variables = models.JSONField(null=True, blank=True, verbose_name='Used Variables')
    latex_data = models.TextField(default=FORMULA_DEFAULT, verbose_name='Latex Data')
    code = models.TextField(default=CODE_DEFOULT, verbose_name='Python Code')
    formula_img = models.ImageField(upload_to='formula/', null=True, blank=True)
    # file = models.FileField(upload_to='files/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def get_formula(self):
        return f"`{self.latex_data}`"
    
    def save(self, *args, **kwargs):
        if self.code:
            variables = get_function_variables(self.code)
            self.variables = variables
        super().save(*args, **kwargs)


class FunksionalData(BaseModel):
    name = models.CharField(max_length=150)
    file = models.FileField(upload_to='funksional_datas/')
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)   
        super().save(*args, **kwargs)
             