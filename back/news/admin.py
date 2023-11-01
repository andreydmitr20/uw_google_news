from django.contrib import admin
from datetime import datetime, timedelta
from config import config
from .models import Clients


class ClientsAdmin(admin.ModelAdmin):
    """ClientsAdmin"""

    list_display = [
        "clients_id",
        "email",
        "news_type",
        "days_in_week",
        "phone",
        "date_created",
        "date_updated",
        "date_payed",
    ]
    # list_filter = [
    #     "is_bad",
    # ]
    search_fields = ["email", "phone", "news_type"]

    def date_created(self, obj):
        if obj.utc_created:
            utc_datetime = datetime.utcfromtimestamp(obj.utc_created) + timedelta(
                hours=config.timezone
            )
            return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

    date_created.short_description = f"Created UTC{config.timezone}"

    def date_updated(self, obj):
        if obj.utc_updated:
            utc_datetime = datetime.utcfromtimestamp(obj.utc_updated) + timedelta(
                hours=config.timezone
            )
            return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

    date_updated.short_description = f"Updated UTC{config.timezone}"

    def date_payed(self, obj):
        if obj.utc_payed:
            utc_datetime = datetime.utcfromtimestamp(obj.utc_payed) + timedelta(
                hours=config.timezone
            )
            return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return "N/A"

    date_payed.short_description = f"Payed UTC{config.timezone}"


admin.site.register(Clients, ClientsAdmin)
