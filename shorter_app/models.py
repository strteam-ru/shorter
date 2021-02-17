from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True, editable=False)


class Links(models.Model):
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
    short_link = models.CharField(max_length=10)
    full_link = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
