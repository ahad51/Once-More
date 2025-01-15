from django.db import models

class CPD(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='cpd_images/')

    def __str__(self):
        return self.title
