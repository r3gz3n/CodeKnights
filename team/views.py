from django.http import HttpResponse
from django.template import loader, Context
from team.models import TeamDetails

def teamPage(request):
    team_details = TeamDetails.objects.all()[0]
    t = loader.get_template('teamPage.html')
    c = Context({'team':team_details})
    return HttpResponse(t.render(c))
