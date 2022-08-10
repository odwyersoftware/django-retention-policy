import uuid
from datetime import timedelta

import pytest
from django.utils import timezone

from django_retention_policy import (
    task_delete_expired_db_records,
)
from tests.example_project.example_app import models

pytestmark = pytest.mark.django_db


class TestTaskDeleteExpiredDbRecords:
    def test(self, freezer):
        data_retention_num_seconds = 86400
        now = timezone.now()

        records_within_retention_period_timestamps = (
            now,
            now - timedelta(seconds=data_retention_num_seconds),
            now - timedelta(seconds=data_retention_num_seconds - 1),
            now - timedelta(seconds=data_retention_num_seconds - 2),
            now - timedelta(seconds=data_retention_num_seconds - 100000),
        )
        records_outside_retention_period_timestamps = (
            now - timedelta(seconds=data_retention_num_seconds + 1),
            now - timedelta(seconds=data_retention_num_seconds + 2),
            now - timedelta(seconds=data_retention_num_seconds + 3),
            now - timedelta(seconds=data_retention_num_seconds + 100000),
        )

        records_within_retention_period = []
        for timestamp in records_within_retention_period_timestamps:
            freezer.move_to(timestamp)
            record = models.ExampleModel.objects.create(
                user_id=str(uuid.uuid4()),
                timestamp=timestamp,
            )
            records_within_retention_period.append(record)

        records_outside_retention_period = []
        for timestamp in records_outside_retention_period_timestamps:
            freezer.move_to(timestamp)
            record = models.ExampleModel.objects.create(
                user_id=str(uuid.uuid4()),
                timestamp=timestamp,
            )
            records_outside_retention_period.append(record)

        result = task_delete_expired_db_records(
            app_name='example_app',
            model_name='ExampleModel',
            time_based_column_name='timestamp',
            data_retention_num_seconds=data_retention_num_seconds,
            now=now,
        )

        assert result == (
            len(records_outside_retention_period),
            {
                'example_app.ExampleModel': len(
                    records_outside_retention_period
                )
            },
        )
        record_pks = models.ExampleModel.objects.all().values_list(
            'pk', flat=True
        )
        assert set(record_pks) == set(
            r.pk for r in records_within_retention_period
        )
