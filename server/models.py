from django.db import models

# Create your models here.
class Servers(models.Model):
    id_server = models.CharField(max_length=1, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id_server