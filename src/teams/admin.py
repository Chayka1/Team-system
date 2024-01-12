from django.contrib import admin

from teams.models import Team
from users.models import User


class UserInline(admin.StackedInline):
    model = User
    extra = 1


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("email", "first_name", "last_name", "teams")


admin.site.register(User, UserAdmin)


class TeamAdmin(admin.ModelAdmin):
    inlines = [UserInline]


admin.site.register(Team, TeamAdmin)
