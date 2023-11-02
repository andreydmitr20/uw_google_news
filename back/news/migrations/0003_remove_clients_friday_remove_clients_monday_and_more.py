# Generated by Django 4.2.6 on 2023-10-30 22:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0002_alter_clients_friday_alter_clients_monday_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clients",
            name="friday",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="monday",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="saturday",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="sunday",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="thursday",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="tuesday",
        ),
        migrations.RemoveField(
            model_name="clients",
            name="wednesday",
        ),
        migrations.AddField(
            model_name="clients",
            name="days_in_week",
            field=models.IntegerField(blank=True, db_index=True, default="1"),
        ),
        migrations.AlterField(
            model_name="clients",
            name="news_type",
            field=models.CharField(blank=True, default="w", max_length=20),
        ),
    ]
