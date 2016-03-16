from django.conf.urls import url
import team.views

urlpatterns = [
    url(r'teampage/', team.views.teamPage),
    url(r'login/', team.views.loginPage),
    url(r'signup', team.views.signupPage),
    url(r'edit', team.views.editPage),
    url(r'logout', team.views.logout)
]
