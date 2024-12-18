from django.db import models

class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('JUNK_MODEL', 'Junk Modelling'),
        ('PHYSICAL', 'Physical Activities'),
        ('PLAY_PROVOCATION', 'Play Provocations'),
        ('WORKSHEETS', 'Worksheets & Games'),
        ('EXTENSIONS', 'Extensions'),
    ]

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='activities/images/', blank=True, null=True)
    instructions = models.TextField()
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes", blank=True, null=True)
    required_materials = models.TextField(help_text="List of materials", blank=True, null=True)
    downloadable_resources = models.FileField(upload_to='activities/resources/', blank=True, null=True)
    curriculum_links = models.TextField(help_text="Curriculum alignment details", blank=True, null=True)
    # engineering_skills = models.TextField(help_text="List of skills developed", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
