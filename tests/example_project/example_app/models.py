from django.utils import timezone
from django.db import models


class ExampleModel(models.Model):
    user_id = models.CharField(max_length=36)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(primary_key=True, auto_now_add=True)

    class Meta:
        db_table = 'example_model'
        unique_together = (
            (
                'user_id',
                'timestamp',
                'type',
            ),
        )
        indexes = [
            models.Index(
                name='%(class)s_idx',
                fields=[
                    'user_id',
                    'type',
                    'timestamp',
                ],
            )
        ]
