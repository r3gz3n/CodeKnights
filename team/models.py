from django.db import models
from django.contrib import admin


class TeamDetails(models.Model):
    teamName = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    member1Name = models.CharField(max_length=50)
    member1Branch = models.CharField(max_length=50)
    member2Name = models.CharField(max_length=50, blank=True)
    member2Branch = models.CharField(max_length=50, blank=True)
    member3Name = models.CharField(max_length=50, blank=True)
    member3Branch = models.CharField(max_length=50, blank=True)

class TeamDetailsAdmin(admin.ModelAdmin):
    list_display = ('teamName', 'password', 'member1Name', 'member1Branch', 'member2Name', 'member2Branch', 'member3Name', 'member3Branch')

admin.site.register(TeamDetails, TeamDetailsAdmin)

