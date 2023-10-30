from django.contrib import admin

from .models import Clients


class ClientsAdmin(admin.ModelAdmin):
    """ClientsAdmin"""

    list_display = [
        "clients_id",
        "email",
        "news_type",
        "days_in_week",
        "phone",
        "utc_created",
        "utc_updated",
        "utc_payed",
    ]
    # list_filter = [
    #     "is_bad",
    # ]
    search_fields = ["email", "phone", "news_type"]


admin.site.register(Clients, ClientsAdmin)
