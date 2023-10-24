from django.db import migrations, models
from django.conf import settings

from dramatiq_pg.schema import generate_init_sql
from django_dramatiq_pg_adapter.utils import get_tablename


SCHEMA = getattr(settings, "DRAMATIQ_PG_SCHEMA", "public")
PREFIX = getattr(settings, "DRAMATIQ_PG_PREFIX", "dramatiq_")


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="PgDramatiqTask",
            fields=[
                ("message_id", models.UUIDField(primary_key=True, serialize=False)),
                ("queue_name", models.TextField(default="default")),
                (
                    "state",
                    models.TextField(
                        choices=[
                            ("queued", "Queued"),
                            ("consumed", "Consumed"),
                            ("rejected", "Rejected"),
                            ("done", "Done"),
                        ],
                        default="queued",
                    ),
                ),
                ("mtime", models.DateTimeField()),
                ("message", models.JSONField()),
                ("result", models.JSONField()),
                ("result_ttl", models.DateTimeField()),
            ],
            options={"db_table": get_tablename(PREFIX), "managed": False},
        ),
        migrations.RunSQL(
            generate_init_sql(
                schema=SCHEMA,
                prefix=PREFIX,
            )
        ),
    ]
