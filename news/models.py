from django.db import models
from django.utils import timezone

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Mobil', 'Mobil'),
        ('Mobil Bekas', 'Mobil Bekas'),
        ('Tips and Trick Otomotif', 'Tips and Trick Otomotif'),
        ('Others', 'Others'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Others')

    def __str__(self):
        return self.title
