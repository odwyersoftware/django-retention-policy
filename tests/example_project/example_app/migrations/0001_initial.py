# Generated by Django 4.0.6 on 2022-08-10 10:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ExampleModel',
            fields=[
                ('user_id', models.CharField(max_length=36)),
                (
                    'created_on',
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ('modified_on', models.DateTimeField(auto_now=True)),
                (
                    'timestamp',
                    models.DateTimeField(
                        auto_now_add=True, primary_key=True, serialize=False
                    ),
                ),
            ],
            options={
                'db_table': 'example_model',
            },
        ),
        migrations.AddIndex(
            model_name='examplemodel',
            index=models.Index(
                fields=['user_id', 'timestamp'], name='examplemodel_idx'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='examplemodel',
            unique_together={('user_id', 'timestamp')},
        ),
    ]
