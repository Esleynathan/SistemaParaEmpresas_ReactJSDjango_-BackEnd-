from django.db import models


class Enterprise(models.Model):
    nome = models.CharField(max_length=150)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)