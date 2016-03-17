from django.db import models
from django.contrib import admin


class Submissions(models.Model):
    teamName = models.CharField(max_length=20)
    submissionTime = models.DateTimeField()
    solution = models.FileField(upload_to='/home/r3gz3n/CodeKnights/allSubmissions')
    problemId = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    verdict = models.CharField(max_length=50)
    timeTaken = models.FloatField()
    memoryTaken = models.FloatField()

class SubmissionsAdmin(admin.ModelAdmin):
    list_display = ('teamName', 'submissionTime', 'solution', 'problemId', 'language', 'verdict', 'timeTaken', 'memoryTaken')

admin.site.register(Submissions, SubmissionsAdmin)
