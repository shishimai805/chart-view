from django.db import models

# Create your models here.
class Code(models.Model):
    num = models.CharField(max_length = 255)
    image = models.ImageField()
    def __str__(self):
        return self.num

    class Meta:
        verbose_name_plural = "Code"
