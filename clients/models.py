from django.db import models

# Client model
class Client(models.Model):
    name = models.CharField(max_length=120)

    def _str_(self):
        return self.name