from django.conf.urls import url
import submissions.views

urlpatterns = [
    url(r'^all', submissions.views.allSubmissionsPage),
    url(r'^my', submissions.views.mySubmissionsPage),
]
