from django.db import models


class TeamDetails(models.Model):
    teamName = models.CharField(max_length=20)
    member1Name = models.CharField(max_length = 50)
    member1Branch = models.CharField(max_length = 50)
    member1Year = models.IntegerField(default = 0)
    member1Email = models.EmailField(max_length = 50)
    member1Phone = models.CharField(max_length = 10)
    member1College = models.CharField(max_length = 50)
    member2Name = models.CharField(max_length = 50)
    member2Branch = models.CharField(max_length = 50)
    member2Year = models.IntegerField(default = 0)
    member3Name = models.CharField(max_length = 50)
    member3Branch = models.CharField(max_length = 50)
    member3Year = models.IntegerField(default = 0)

