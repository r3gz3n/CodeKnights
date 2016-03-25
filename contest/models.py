from django.db import models
from django.contrib import admin


class Problems(models.Model):
    problemId = models.CharField(max_length = 50)
    problemTitle = models.CharField(max_length = 50)
    problemPath = models.FilePathField(path = '/home/r3gz3n/CodeKnights/problems', allow_folders = True)

class Ranklist(models.Model):


class ProblemsAdmin(admin.ModelAdmin):
    list_display = ('problemTitle', 'problemPath')

clas RanklistAdmin(admin.ModelAdmin):
    list_display = ()

admin.site.register(Problems, ProblemsAdmin)
admin.site.register(Ranklist, RanklistAdmin)

