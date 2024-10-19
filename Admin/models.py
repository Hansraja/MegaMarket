from django.db import models
from nanoid import generate

# Create your models here.

class Brand(models.Model):
    id = models.CharField(max_length=100, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ForeignKey('Common.Image', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        if not self.pk:
            self.id = generate(size=28)
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'brand'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'