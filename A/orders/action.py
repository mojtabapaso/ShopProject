from django.contrib import admin
@admin.action(description='فعال تخفیف')
def activer(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='غیر فعال تخفیف')
def deactiver(modeladmin, request, queryset):
    queryset.update(is_active=False)
