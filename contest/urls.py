from django.conf.urls import url
import contest.views

urlpatterns = [
    url(r'^firstcontest', contest.views.contestPage),
    url(r'^problems$', contest.views.problemPage),
    url(r'^submit', contest.views.submitPage),
    url(r'ranklist', contest.views.ranklistPage),
]
