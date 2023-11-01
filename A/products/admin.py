from django.contrib import admin
from .models import Brand, Products, Commend

admin.site.register(Brand)
admin.site.register(Products)


@admin.action(description='فعال کردن')
def activer(modeladmin, request, queryset):
    queryset.update(active=True)


class CommendActive(admin.ModelAdmin):
    actions = [activer]


admin.site.register(Commend, CommendActive)
