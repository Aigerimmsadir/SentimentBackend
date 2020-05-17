from django.db import models


class Comment(models.Model):
    comment_id = models.CharField(max_length=1000, primary_key=True)
    message = models.TextField(null=True, blank=True)
