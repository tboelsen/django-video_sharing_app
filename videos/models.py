from django.db import models
from django.contrib.auth import get_user_model

class Theme(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    youtube_id = models.CharField(max_length=250)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
