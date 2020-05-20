from django.db import models


class Comment(models.Model):
    comment_id = models.CharField(max_length=1000)
    comment_date=models.CharField(max_length=1000, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
