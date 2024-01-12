from django.db import models

from teams.models import Team


class User(models.Model):
    email = models.EmailField(max_length=150, unique=True, null=False)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    teams = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.email
