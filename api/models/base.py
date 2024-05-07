# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Manual(models.Model):
    TITLE_MAX_LENGTH = 255
    UPLOAD_TO = 'manuals/'
    DEFAULT_TITLE = "New Manual"

    title = models.CharField(max_length=TITLE_MAX_LENGTH, default=DEFAULT_TITLE)
    file = models.FileField(upload_to=UPLOAD_TO)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title