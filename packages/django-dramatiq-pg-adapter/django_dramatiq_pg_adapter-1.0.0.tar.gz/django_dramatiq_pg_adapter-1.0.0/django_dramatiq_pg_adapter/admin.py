from django.contrib import admin
from django_dramatiq_pg_adapter.models import PgDramatiqTask


class ActorFilter(admin.SimpleListFilter):
    title = "Actor"
    parameter_name = "actor"
    lookup = "message__actor_name"

    def lookups(self, request, model_admin):
        qset = model_admin.model.objects.values_list(self.lookup, flat=True).distinct()
        return [(x, x) for x in qset]

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name)
        if value is None:
            return queryset
        return queryset.filter(**{self.lookup: value})


@admin.register(PgDramatiqTask)
class PgDramatiqTaskAdmin(admin.ModelAdmin):
    list_display = (
        "message_id",
        "queue_name",
        "actor",
        "state",
    )
    list_filter = (
        "queue_name",
        ActorFilter,
        "state",
    )

    def actor(self, obj: PgDramatiqTask) -> str:
        return obj.message["actor_name"]

    actor.admin_order_field = "message__actor_name"
