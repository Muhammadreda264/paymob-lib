# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    date = models.DateField()
    category = models.CharField(max_length=50)
    url = models.URLField()