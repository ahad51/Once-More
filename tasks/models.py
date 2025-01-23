from django.db import models

class Topics(models.Model):
    CATEGORY_CHOICES = [
        ('INTRODUCTION TO ENGENEERING', 'Introduction to Engineering'),
        ('SPACE', 'Space'),
        ('ROBOTS', 'Robots'),
        ('NATURE', 'Nature'),
        ('MEDICINE', 'Medicine'),
        ('STRUCTURE', 'Structure'),
        ('CHEMISTRY', 'Chemistry'),
        ('ENERGY', 'Energy'),
        ('MATERIAL', 'Material'),
        ('LIGHTS', 'Lights'),


    ]
    title = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='activities/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    