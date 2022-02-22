from os import path
from pathlib import Path
from django.db import models
import uuid

from django.db.models.fields.files import FileField

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=128)
    file = FileField(upload_to='excels')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
