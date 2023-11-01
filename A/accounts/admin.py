from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'is_admin')
    list_filter = ()
    fieldsets = (
        ( {'اطلاعات کلی': ('phone_number', 'password')}),
        ('مجوز ها و دسترسی ها', {'fields': ('is_admin', 'last_login')})
    )

    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('password1', 'password2'), }),)
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()
    readonly_fields = ('last_login',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', "id", "date_of_berth", "first_name", "last_name", "email", "address")
    fieldsets = (
        ("کاربر", {'fields': ('name', "id")}),
        ('جزییات', {'fields': ("date_of_berth", 'first_name', 'last_name', "email")}),
        ('آدرس', {'fields': ('address',)}),
    )


