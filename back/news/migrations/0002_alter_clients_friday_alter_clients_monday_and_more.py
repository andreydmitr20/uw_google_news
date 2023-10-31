# Generated by Django 4.2.6 on 2023-10-30 18:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clients",
            name="friday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
        migrations.AlterField(
            model_name="clients",
            name="monday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
        migrations.AlterField(
            model_name="clients",
            name="saturday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
        migrations.AlterField(
            model_name="clients",
            name="sunday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
        migrations.AlterField(
            model_name="clients",
            name="thursday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
        migrations.AlterField(
            model_name="clients",
            name="tuesday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
        migrations.AlterField(
            model_name="clients",
            name="wednesday",
            field=models.CharField(blank=True, db_index=True, default="", max_length=5),
        ),
    ]