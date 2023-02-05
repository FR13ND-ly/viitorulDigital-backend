from django.conf import settings
from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    imageUrl = models.TextField(default='')

    def __str__(self):
        return self.title + " #" + str(self.id)

class Comment(models.Model):
    author = models.TextField(null=True)
    text = models.TextField(null=True)
    imageURL = models.TextField(null=True)
    article = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Profile(models.Model):
    token = models.TextField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    article = models.TextField(null=True)
    user = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)