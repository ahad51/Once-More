from django.db import models

class HowItWorks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to='how_it_works_attachments/')
    image = models.ImageField(upload_to='how_it_works_images/')
    
    def __str__(self):
        return self.title
