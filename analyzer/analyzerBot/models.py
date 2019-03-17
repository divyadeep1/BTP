from django.db import models

class Review(models.Model):
    product_name=models.CharField(max_length=5000, null=True, blank=True)
    file = models.FileField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.product_name