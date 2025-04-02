from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.common.models import BaseModel
from datetime import datetime, timedelta
import uuid
# Create your models here.
USER_STATUS_CHOICES = (
    ('free', 'FREE'),
    ('premium', 'PREMIUM'),

)


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='free')

    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = datetime.now().date()
        birth_year = self.birth.year
        day1 = self.birth.strftime("%j")
        day2 = today.strftime("%j")

        return f"{((today.year-birth_year) if day2 <= day1 else (today.year - birth_year - 1))}"
    
    def __str__(self):  
        return f"{self.email}"

email_expire_time = 5

class UserResetPassword(BaseModel):
    email = models.EmailField(blank=True, unique=False, null=True)

    def __str__(self):
        return f"{self.email}"
    