from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "teams"

    def __str__(self):
        return self.name
