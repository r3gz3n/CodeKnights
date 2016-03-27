from django.db import models
from django.contrib import admin


class Problems(models.Model):
    problemId = models.CharField(max_length = 50)
    problemTitle = models.CharField(max_length = 50)
    problemPath = models.FilePathField(path = '/home/r3gz3n/CodeKnights/problems', allow_folders = True)


class Ranklist(models.Model):
    teamName = models.CharField(max_length = 100)
    totalTime = models.IntegerField(default = 0)
    totalWA = models.IntegerField(default = 0)
    score = models.IntegerField(default = 0)
    problem1score = models.BooleanField(default = False)
    problem1WA = models.IntegerField(default = 0)
    problem2score = models.BooleanField(default = False)
    problem2WA = models.IntegerField(default = 0)
    problem3score = models.BooleanField(default = False)
    problem3WA = models.IntegerField(default = 0)


class ProblemsAdmin(admin.ModelAdmin):
    list_display = ('problemTitle', 'problemPath')

class RanklistAdmin(admin.ModelAdmin):
    list_display = ('teamName', 'totalTime', 'totalWA', 'score', 'problem1WA', 'problem1score', 'problem2WA', 'problem2score', 'problem3WA', 'problem3score')

admin.site.register(Problems, ProblemsAdmin)
admin.site.register(Ranklist, RanklistAdmin)

