from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Photo(models.Model):
    photo = models.ImageField(upload_to='user_photos', blank=True, null=True)
    result_photo = models.ImageField(upload_to='user_photos', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    file_results = models.FileField(blank=True, upload_to='user_photos_results')

    def get_absolute_url(self):
        return reverse('photo-detail', kwargs={'pk': self.pk})