from django.db import models

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('JUNK_MODEL', 'Junk Modelling'),
        ('PHYSICAL', 'Physical Activities'),
        ('PLAY_PROVOCATION', 'Play Provocations'),
        ('WORKSHEETS', 'Worksheets & Games'),
        ('EXTENSIONS', 'Extensions'),
        ('TEACHER_OVERVIEW', 'Teacher Overview'),
        ('ENGINEER ROLE MODEL', 'Engineer Role Model'),
        ('TEACHER_OVERVIEW', 'Teacher Overview'),
        ('STORY', 'Story'),


    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/images/', blank=True, null=True)
    downloadable_resources = models.FileField(upload_to='activities/resources/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
