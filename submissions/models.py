from django.db import models
from django.contrib import admin


class Submissions(models.Model):
    teamName = models.CharField(max_length=100)
    submissionTime = models.CharField(max_length=20)
    problemId = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    verdict = models.CharField(max_length=50)
    timeTaken = models.FloatField()
    memoryTaken = models.IntegerField()

class SubmissionsAdmin(admin.ModelAdmin):
    list_display = ('teamName', 'submissionTime', 'problemId', 'language', 'verdict', 'timeTaken', 'memoryTaken')

admin.site.register(Submissions, SubmissionsAdmin)

