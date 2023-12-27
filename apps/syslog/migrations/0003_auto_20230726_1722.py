# Generated by Django 2.2.6 on 2023-07-26 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("syslog", "0002_node_probejob"),
    ]

    operations = [
        migrations.AddField(
            model_name="alarmstrategy",
            name="is_scheduled",
            field=models.BooleanField(default=True, verbose_name="是否开启"),
        ),
        migrations.AddField(
            model_name="alarmstrategy",
            name="title",
            field=models.CharField(db_index=True, default="", max_length=200, verbose_name="策略标题"),
        ),
    ]