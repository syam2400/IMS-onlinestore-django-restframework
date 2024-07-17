import uuid
from django.db import models
from versatileimagefield.fields import VersatileImageField
from django.utils.translation import gettext_lazy as _

class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    ProductID = models.BigIntegerField(unique=True)    
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)    
    ProductImage = VersatileImageField(upload_to="uploads/", blank=True, null=True)    
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey("auth.User", related_name="user%(class)s_objects", on_delete=models.CASCADE,blank=True, null=True)    
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)    
    HSNCode = models.CharField(max_length=255, blank=True, null=True)    
    TotalStock = models.IntegerField(null=True,blank=True)
  
    class Meta:
        db_table = "products_product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")
        indexes = [
            models.Index(fields=['ProductName']),
            models.Index(fields=['CreatedDate']),
        ]

    def __str__(self):
        return f'{self.ProductName}-{self.ProductCode}'

    
class Variant(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=100)
    

    class Meta:
        unique_together = (('product', 'variant_name'),)
        indexes = [
            models.Index(fields=['product', 'variant_name']),
        ]
    
    def __str__(self):
        return f'{self.product.ProductCode}-{self.product.ProductName} - {self.variant_name}'
    

class SubVariant(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='subvariants',null=True,blank=True)
    option = models.CharField(max_length=255,null=True,blank=True)
    stock = models.IntegerField(null=True,blank=True)

    class Meta:
        unique_together = (('variant', 'option'),)
        indexes = [
            models.Index(fields=['variant', 'option']),
        ]
        
    def __str__(self):
        return f'{self.option}-{self.variant.product.ProductName}-{self.variant.product.ProductCode}'

