from django.db import models

class Curriculum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to='curriculum_images/')
    
    def __str__(self):
        return self.title
