from django.db import models
from django.contrib.postgres.fields import JSONField  # For Postgres JSON data

class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_data = models.JSONField(blank=True, null=True)  # Store parsed Excel content

    def __str__(self):
        return self.file_name
