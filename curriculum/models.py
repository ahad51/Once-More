from django.conf import settings
from django.db import models

class Curriculum(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    standards_document = models.FileField(upload_to='curriculum_documents/')

    def __str__(self):
        return self.name


class CPDModule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    topics = models.TextField()
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class CPDProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey('CPDModule', on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.module.title}"
2
