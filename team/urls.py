from django.conf.urls import url
import team.views

urlpatterns = [
    url(r'teampage/', team.views.teamPage),
]
