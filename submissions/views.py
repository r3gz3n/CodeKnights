from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from submissions.models import Submissions

class SubmissionDetails(object):
    def __init__(self, teamName, problemTitle, submissionTime, verdict, language, timeTaken, memoryTaken):
        self.teamName = teamName
        self.problemTitle = problemTitle
        self.submissionTime = submissionTime
        self.verdict = verdict
        self.language = language
        self.timeTaken = timeTaken
        self.memoryTaken = memoryTaken

def allSubmissionsPage(request):
    try:
        team_name = request.session['team_name']
    except KeyError:
        return HttpResponseRedirect('http://localhost:8000/team/login')
    all_submissions = Submissions.objects.all()
    all_submissions_details = list()
    for submission in all_submissions:
        teamName = submission.teamName
        problemTitle = submission.problemId.replace('_', ' ')
        submissionTime = submission.submissionTime
        verdict = submission.verdict
        language = submission.language
        timeTaken = submission.timeTaken
        memoryTaken = submission.memoryTaken
        all_submissions_details.append(SubmissionDetails(teamName, problemTitle, submissionTime, verdict, language, timeTaken, memoryTaken))
    t = loader.get_template('allSubmissionsPage.html')
    c = Context({'allSubmissions':all_submissions_details})
    return HttpResponse(t.render(c))

def mySubmissionsPage(request):
    try:
        team_name = request.session['team_name']
    except KeyError:
        return HttpResponseRedirect('http://localhost:8000/team/login')
    my_submissions = Submissions.objects.get(teamName = team_name)
    mySubmissionDetails = list()
    for submission in my_submissions:
        solutions = submission.teamName
        problemTitle = submission.problemId.replace('_', ' ')
        submissionTime = submission.submissionTime
        verdict = submission.verdict
        language = submission.language
        timeTaken = submission.timeTaken
        memoryTaken = submission.memoryTaken
        my_submissions_details.append(MySubmissionDetails(teamName, problemTitle, submissionTime, verdict, language, timeTaken, memoryTaken))
    t = loader.get_template('mySubmissionsPage.html')
    c = Context({'mySubmissions':my_submissions_details})
    return HttpResponse(t.render(c))

