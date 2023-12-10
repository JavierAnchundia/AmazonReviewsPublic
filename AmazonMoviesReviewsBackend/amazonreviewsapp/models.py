from django.db import models
from django_unixdatetimefield import UnixDateTimeField

# Create your models here.

class Review(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    productId = models.TextField()
    userId = models.TextField()
    profileName = models.TextField()
    helpfulness = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score = models.IntegerField(default=0)
    time = models.DateTimeField()
    summary = models.TextField()
    text = models.TextField()