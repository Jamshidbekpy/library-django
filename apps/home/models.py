from django.db import models
from apps.common.models import BaseModel
from apps.resources.models import Resource

# Create your models here.

class Contact(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name}-{self.email}"


class Subscribe(BaseModel):
    email = models.EmailField()

    def __str__(self):
        return self.email
    

class Favourite(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='favourites')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='favourites')
    
    def __str__(self):
        return f"{self.user}-{self.resource}"
    
    class Meta:
        unique_together = ['user', 'resource']
        
