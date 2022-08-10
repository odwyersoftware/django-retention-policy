# django-retention-policy

Deletes Django database records according to a retention policy of your choice.

## Installation

```bash
pip install django-retention-policy
```

And setup the periodic Celery task, in your [settings.py](https://docs.djangoproject.com/en/4.1/ref/settings/):

```python
from datetime import timedelta

EIGHT_WEEKS_IN_SECS = 86400 * 7 * 8
CELERY_BEAT_SCHEDULE = {
    'periodic-task_delete_expired_db_records': {
        'task': 'django_retention_policy.task_delete_expired_db_records',
        'schedule': timedelta(hours=12),
        'kwargs': {
            'app_name': 'django_app_name_here',
            'model_name': 'YourDjangoModelNameHere',
            'time_based_column_name': 'timestamp',
            'data_retention_num_seconds': EIGHT_WEEKS_IN_SECS,
        },
    },
}
CELERY_IMPORTS = (
    'django_retention_policy',
)
```

That's it. Start up your Celery worker, and Celery beat processes and the automatic deletion will take place according to your configuration.
