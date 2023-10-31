from django.db import models


class Clients(models.Model):
    """Clients"""

    clients_id = models.BigAutoField(
        primary_key=True,
        # default=0,
        db_column="clients_id",
    )
    email = models.CharField(
        max_length=200,
        null=False,
        blank=True,
        unique=True,
        default="",
    )
    news_type = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        default="w",
    )
    days_in_week = models.IntegerField(
        null=False,
        blank=True,
        db_index=True,  # non unique index
        unique=False,
        default=1,
    )
    phone = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        # unique=True,
        default="",
    )
    utc_created = models.BigIntegerField(null=False, blank=True, default=0)
    utc_updated = models.BigIntegerField(null=False, blank=True, default=0)
    utc_payed = models.BigIntegerField(null=False, blank=True, default=0)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = "Clients"
