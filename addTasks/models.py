from django.db import models

class AddTask(models.Model):
    CATEGORY_CHOICES = [
        ('ENGINEER ROLE MODEL', 'Engineer Role Model'),
        ('STORY', 'Story'),
        ('EXPLAINER', 'Explainer'),
        ('ACTIVITY 1', 'Activity 1'),
        ('ACTIVITY 2', 'Activity 2'),
        ('ACTIVITY 3 ', 'Activity 3'),
        ('JUNK MODELLING', 'Junk Modelling'),
        ('PHYSICAL ACTIVITIES', 'Physical Activities'),
        ('PLAY PROVOCATIONS', 'Play Provocations'),
        ('WORKSHEETS', 'Worksheets'),
        ('GAMES', 'Games'),
        ('EXTENSIONS', 'Extensions'),



    ]
    title = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='activities/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
