from django.db import models
from django.utils import timezone
# from django.utils.timezone.now import timezone
# from django.core.urlresolver import reverse
# from django.urls import reverse

class Post(models.Model):
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='', blank=True)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    date = models.DateField(null=True)

    def __str__(self):
        return self.title
