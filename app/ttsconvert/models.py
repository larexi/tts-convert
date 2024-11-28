from django.contrib.auth.models import User
from django.db import models

STATUSES = [
    ('CREATED', 'Created'),
    ('PROCESSING', 'Processing'),
    ('FINISHED', 'Finished'),
    ('CANCELED', 'Canceled'),
    ('ERROR', 'Error'),
]

class ConversionRequest(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default='CREATED', max_length=20)
    text_to_convert = models.TextField()
    results = models.TextField(default='')
