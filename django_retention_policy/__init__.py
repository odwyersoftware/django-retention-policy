import logging
import time
from datetime import timedelta

from django.apps import apps
from django.utils import timezone
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def task_delete_expired_db_records(
    app_name,
    model_name,
    time_based_column_name,
    data_retention_num_seconds,
    now=None,
):
    logger.info(
        'Checking for %s %s DB records to delete which are '
        'beyond retention period...',
        app_name,
        model_name,
    )
    start_time = time.time()
    model_class = apps.get_model(app_label=app_name, model_name=model_name)
    now = now or timezone.now()
    min_age_records_to_delete = now - timedelta(
        seconds=data_retention_num_seconds
    )
    logger.info(
        'Executing delete query on %s %s records older than %s...',
        app_name,
        model_name,
        min_age_records_to_delete,
    )
    deleted_records = model_class.objects.filter(
        **{f'{time_based_column_name}__lt': min_age_records_to_delete}
    ).delete()
    took = time.time() - start_time
    logger.info(
        'Done deleting %s %s DB records to delete which are '
        'beyond retention period. Took %s secs. Result: %s',
        app_name,
        model_name,
        took,
        deleted_records,
    )
    return deleted_records
