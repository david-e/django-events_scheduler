from django.contrib import admin

import models


class EventTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.EventType, EventTypeAdmin)


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Event, EventAdmin)
